from datetime import date

import pytest

from src.core.exceptions import ValidationException
from src.schemas.expense_schema import ExpenseCreateSchema
from src.services.expense_service import ExpenseService


class FakeExpenseRepository:
    def create(self, entity):
        return entity

    def get_all(self):
        return []

    def get_by_month(self, year, month):
        return []

    def get_by_category(self, category_id):
        return []


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
