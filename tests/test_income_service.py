from datetime import date

import pytest

from src.core.exceptions import ValidationException
from src.schemas.income_schema import IncomeCreateSchema
from src.services.income_service import IncomeService


class FakeIncomeRepository:
    def create(self, entity):
        return entity

    def get_all(self):
        return []

    def get_by_month(self, year, month):
        return []


class FakeCategoryRepository:
    def get_by_id(self, entity_id):
        return {"id": entity_id}


def test_create_income_requires_positive_amount():
    service = IncomeService(FakeIncomeRepository(), FakeCategoryRepository())

    with pytest.raises(ValidationException):
        service.create_income(IncomeCreateSchema(amount=0, source="Salary", income_date=date.today()))


def test_create_income_requires_source():
    service = IncomeService(FakeIncomeRepository(), FakeCategoryRepository())

    with pytest.raises(ValidationException):
        service.create_income(IncomeCreateSchema(amount=100, source="", income_date=date.today()))
