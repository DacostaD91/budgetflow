from src.analytics.budget_analysis import (
    calculate_budget_difference,
    calculate_budget_usage_percentage,
    get_budget_status,
)
from src.core.exceptions import NotFoundException, ValidationException
from src.models.monthly_budget import MonthlyBudget
from src.repositories.budget_repository import BudgetRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.expense_repository import ExpenseRepository
from src.schemas.budget_schema import MonthlyBudgetCreateSchema, MonthlyBudgetUpdateSchema
from src.utils.validators import validate_positive_amount


class BudgetService:
    def __init__(
        self,
        budget_repository: BudgetRepository,
        category_repository: CategoryRepository,
        expense_repository: ExpenseRepository,
    ):
        self.budget_repository = budget_repository
        self.category_repository = category_repository
        self.expense_repository = expense_repository

    def create_monthly_budget(self, budget_data: MonthlyBudgetCreateSchema) -> MonthlyBudget:
        self._validate_budget_period(budget_data.year, budget_data.month)
        validate_positive_amount(budget_data.planned_amount)
        category = self._get_valid_expense_category(budget_data.category_id)

        existing_budget = self.budget_repository.get_by_category_month(
            budget_data.year,
            budget_data.month,
            category.id,
        )
        if existing_budget:
            raise ValidationException("A budget already exists for this category and period.")

        budget = MonthlyBudget(
            year=budget_data.year,
            month=budget_data.month,
            category_id=category.id,
            planned_amount=budget_data.planned_amount,
        )
        return self.budget_repository.create(budget)

    def update_monthly_budget(self, budget_id: int, budget_data: MonthlyBudgetUpdateSchema) -> MonthlyBudget:
        budget = self.budget_repository.get_by_id(budget_id)
        if not budget:
            raise NotFoundException("Budget not found.")

        validate_positive_amount(budget_data.planned_amount)
        budget.planned_amount = budget_data.planned_amount
        return self.budget_repository.update(budget)

    def delete_monthly_budget(self, budget_id: int) -> None:
        budget = self.budget_repository.get_by_id(budget_id)
        if not budget:
            raise NotFoundException("Budget not found.")

        self.budget_repository.delete(budget)

    def get_monthly_budgets(self, year: int, month: int):
        self._validate_budget_period(year, month)
        return self.budget_repository.get_by_month(year, month)

    def get_budget_vs_actual(self, year: int, month: int) -> list[dict]:
        self._validate_budget_period(year, month)
        budgets = self.budget_repository.get_by_month(year, month)
        expenses = self.expense_repository.get_by_month(year, month)
        actual_by_category = self._group_expenses_by_category(expenses)

        result = []
        for budget in budgets:
            actual_amount = actual_by_category.get(budget.category_id, 0)
            difference = calculate_budget_difference(budget.planned_amount, actual_amount)
            usage_percentage = calculate_budget_usage_percentage(budget.planned_amount, actual_amount)
            result.append(
                {
                    "budget_id": budget.id,
                    "category_id": budget.category_id,
                    "category_name": budget.category.name if budget.category else "",
                    "planned_amount": budget.planned_amount,
                    "actual_amount": actual_amount,
                    "difference": difference,
                    "usage_percentage": usage_percentage,
                    "status": get_budget_status(usage_percentage),
                }
            )

        return result

    def get_monthly_budget_summary(self, year: int, month: int) -> dict:
        budget_vs_actual = self.get_budget_vs_actual(year, month)
        total_planned = sum(item["planned_amount"] for item in budget_vs_actual)
        total_actual = sum(item["actual_amount"] for item in budget_vs_actual)
        difference = calculate_budget_difference(total_planned, total_actual)
        usage_percentage = calculate_budget_usage_percentage(total_planned, total_actual)
        overbudget_categories = sum(1 for item in budget_vs_actual if item["actual_amount"] > item["planned_amount"])

        return {
            "total_planned": total_planned,
            "total_actual": total_actual,
            "difference": difference,
            "usage_percentage": usage_percentage,
            "overbudget_categories": overbudget_categories,
        }

    def _validate_budget_period(self, year: int, month: int) -> None:
        if year < 1:
            raise ValidationException("Year must be valid.")
        if month < 1 or month > 12:
            raise ValidationException("Month must be between 1 and 12.")

    def _get_valid_expense_category(self, category_id: int):
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise ValidationException("Category does not exist.")
        if category.type != "expense":
            raise ValidationException("Only expense categories can be budgeted.")
        return category

    def _group_expenses_by_category(self, expenses) -> dict[int, float]:
        actual_by_category: dict[int, float] = {}
        for expense in expenses:
            actual_by_category[expense.category_id] = actual_by_category.get(expense.category_id, 0) + expense.amount
        return actual_by_category
