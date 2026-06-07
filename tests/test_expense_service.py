from datetime import date

import pytest

from src.core.exceptions import ValidationException
from src.schemas.expense_schema import ExpenseCreateSchema
from src.services.expense_service import ExpenseService


class FakeExpenseRepository:
    def __init__(self):
        self.entity = None

    def create(self, entity):
        self.entity = entity
        return entity

    def get_by_id(self, entity_id):
        return self.entity

    def get_all(self):
        return []

    def get_by_month(self, year, month):
        return []

    def get_by_category(self, category_id):
        return []

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
