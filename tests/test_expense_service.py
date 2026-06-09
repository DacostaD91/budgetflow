from datetime import date

import pytest

from src.core.exceptions import ValidationException
from src.schemas.expense_schema import ExpenseCreateSchema
from src.services.expense_service import ExpenseService


class FakeExpenseRepository:
    def __init__(self):
        self.entity = None
        self.entities = []

    def create(self, entity):
        self.entity = entity
        self.entities.append(entity)
        return entity

    def get_by_id(self, entity_id):
        return self.entity

    def get_all(self):
        return self.entities

    def get_by_month(self, year, month):
        return [
            entity
            for entity in self.entities
            if entity.expense_date.year == year and entity.expense_date.month == month
        ]

    def get_by_category(self, category_id):
        return []

    def get_recurring_before_month(self, year, month):
        target_date = date(year, month, 1)
        return [
            entity
            for entity in self.entities
            if entity.is_recurring and entity.expense_date < target_date
        ]

    def commit(self):
        pass


class FakeCategoryRepository:
    def get_by_id(self, entity_id):
        return {"id": entity_id}


def test_create_expense_requires_positive_amount():
    service = ExpenseService(FakeExpenseRepository(), FakeCategoryRepository())

    with pytest.raises(ValidationException):
        service.create_expense(ExpenseCreateSchema(amount=0, category_id=1, expense_date=date.today()))


def test_create_expense_requires_category():
    service = ExpenseService(FakeExpenseRepository(), FakeCategoryRepository())

    with pytest.raises(ValidationException):
        service.create_expense(ExpenseCreateSchema(amount=100, category_id=0, expense_date=date.today()))


def test_update_expense_updates_existing_record():
    repository = FakeExpenseRepository()
    service = ExpenseService(repository, FakeCategoryRepository())
    expense = service.create_expense(ExpenseCreateSchema(amount=100, category_id=1, expense_date=date.today()))

    updated = service.update_expense(
        expense.id,
        ExpenseCreateSchema(amount=175, category_id=1, expense_date=date.today(), payment_method="Card"),
    )

    assert updated.amount == 175
    assert updated.payment_method == "Card"


def test_generate_recurring_expenses_for_month_creates_missing_expense():
    repository = FakeExpenseRepository()
    service = ExpenseService(repository, FakeCategoryRepository())
    service.create_expense(
        ExpenseCreateSchema(
            amount=250,
            category_id=1,
            expense_date=date(2026, 6, 30),
            payment_method="Card",
            description="Gym",
            is_recurring=True,
        )
    )

    created = service.generate_recurring_expenses_for_month(2026, 7)

    assert len(created) == 1
    assert created[0].expense_date == date(2026, 7, 30)
    assert created[0].is_recurring is True


def test_generate_recurring_expenses_for_month_avoids_duplicates():
    repository = FakeExpenseRepository()
    service = ExpenseService(repository, FakeCategoryRepository())
    service.create_expense(
        ExpenseCreateSchema(
            amount=250,
            category_id=1,
            expense_date=date(2026, 6, 15),
            payment_method="Card",
            description="Gym",
            is_recurring=True,
        )
    )
    service.generate_recurring_expenses_for_month(2026, 7)

    created_again = service.generate_recurring_expenses_for_month(2026, 7)

    assert created_again == []
