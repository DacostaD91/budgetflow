from datetime import date

import pytest

from src.core.exceptions import ValidationException
from src.schemas.income_schema import IncomeCreateSchema
from src.services.income_service import IncomeService


class FakeIncomeRepository:
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

    def commit(self):
        pass


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


def test_update_income_updates_existing_record():
    repository = FakeIncomeRepository()
    service = IncomeService(repository, FakeCategoryRepository())
    income = service.create_income(IncomeCreateSchema(amount=100, source="Salary", income_date=date.today()))

    updated = service.update_income(
        income.id,
        IncomeCreateSchema(amount=150, source="Bonus", income_date=date.today()),
    )

    assert updated.amount == 150
    assert updated.source == "Bonus"
