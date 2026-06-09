from dataclasses import dataclass

import pytest

from src.core.exceptions import ValidationException
from src.schemas.budget_schema import MonthlyBudgetCreateSchema
from src.services.budget_service import BudgetService


@dataclass
class FakeCategory:
    id: int
    name: str
    type: str


@dataclass
class FakeBudget:
    id: int
    year: int
    month: int
    category_id: int
    planned_amount: float
    category: FakeCategory


@dataclass
class FakeExpense:
    category_id: int
    amount: float


class FakeBudgetRepository:
    def __init__(self):
        self.budgets = []
        self.next_id = 1

    def create(self, budget):
        category = FakeCategory(budget.category_id, f"Category {budget.category_id}", "expense")
        fake_budget = FakeBudget(
            id=self.next_id,
            year=budget.year,
            month=budget.month,
            category_id=budget.category_id,
            planned_amount=budget.planned_amount,
            category=category,
        )
        self.next_id += 1
        self.budgets.append(fake_budget)
        return fake_budget

    def get_by_id(self, budget_id):
        return next((budget for budget in self.budgets if budget.id == budget_id), None)

    def get_by_month(self, year, month):
        return [budget for budget in self.budgets if budget.year == year and budget.month == month]

    def get_by_category_month(self, year, month, category_id):
        return next(
            (
                budget
                for budget in self.budgets
                if budget.year == year and budget.month == month and budget.category_id == category_id
            ),
            None,
        )

    def update(self, budget):
        return budget

    def delete(self, budget):
        self.budgets.remove(budget)


class FakeCategoryRepository:
    def __init__(self, categories=None):
        self.categories = categories or {
            1: FakeCategory(1, "Food", "expense"),
            2: FakeCategory(2, "Salary", "income"),
        }

    def get_by_id(self, category_id):
        return self.categories.get(category_id)


class FakeExpenseRepository:
    def __init__(self, expenses=None):
        self.expenses = expenses or []

    def get_by_month(self, year, month):
        return self.expenses


def build_service(expenses=None, categories=None):
    budget_repository = FakeBudgetRepository()
    service = BudgetService(
        budget_repository,
        FakeCategoryRepository(categories),
        FakeExpenseRepository(expenses),
    )
    return service, budget_repository


def test_create_budget_requires_positive_amount():
    service, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_monthly_budget(MonthlyBudgetCreateSchema(2026, 6, 1, 0))


def test_create_budget_requires_month_greater_than_zero():
    service, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_monthly_budget(MonthlyBudgetCreateSchema(2026, 0, 1, 1000))


def test_create_budget_requires_month_less_than_thirteen():
    service, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_monthly_budget(MonthlyBudgetCreateSchema(2026, 13, 1, 1000))


def test_create_budget_requires_existing_category():
    service, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_monthly_budget(MonthlyBudgetCreateSchema(2026, 6, 99, 1000))


def test_create_budget_rejects_income_category():
    service, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_monthly_budget(MonthlyBudgetCreateSchema(2026, 6, 2, 1000))


def test_create_budget_rejects_duplicate_category_month():
    service, _ = build_service()
    service.create_monthly_budget(MonthlyBudgetCreateSchema(2026, 6, 1, 1000))

    with pytest.raises(ValidationException):
        service.create_monthly_budget(MonthlyBudgetCreateSchema(2026, 6, 1, 1200))


def test_create_budget_allows_valid_budget():
    service, _ = build_service()

    budget = service.create_monthly_budget(MonthlyBudgetCreateSchema(2026, 6, 1, 1000))

    assert budget.planned_amount == 1000
    assert budget.category_id == 1


def test_get_budget_vs_actual_calculates_values():
    expenses = [FakeExpense(category_id=1, amount=250), FakeExpense(category_id=1, amount=550)]
    service, _ = build_service(expenses=expenses)
    service.create_monthly_budget(MonthlyBudgetCreateSchema(2026, 6, 1, 1000))

    result = service.get_budget_vs_actual(2026, 6)

    assert result == [
        {
            "budget_id": 1,
            "category_id": 1,
            "category_name": "Category 1",
            "planned_amount": 1000,
            "actual_amount": 800,
            "difference": 200,
            "usage_percentage": 80,
            "status": "Cuidado",
        }
    ]
