from datetime import date

import pytest

from src.core.exceptions import ValidationException
from src.schemas.income_schema import IncomeCreateSchema
from src.services.income_service import IncomeService


class FakeIncomeRepository:
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
            if entity.income_date.year == year and entity.income_date.month == month
        ]

    def get_recurring_before_month(self, year, month):
        target_date = date(year, month, 1)
        return [
            entity
            for entity in self.entities
            if entity.is_recurring and entity.income_date < target_date
        ]

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


def test_generate_recurring_incomes_for_month_creates_missing_income():
    repository = FakeIncomeRepository()
    service = IncomeService(repository, FakeCategoryRepository())
    service.create_income(
        IncomeCreateSchema(
            amount=1000,
            source="Salary",
            income_date=date(2026, 6, 30),
            category_id=1,
            description="Monthly salary",
            is_recurring=True,
        )
    )

    created = service.generate_recurring_incomes_for_month(2026, 7)

    assert len(created) == 1
    assert created[0].income_date == date(2026, 7, 30)
    assert created[0].is_recurring is True


def test_generate_recurring_incomes_for_month_avoids_duplicates():
    repository = FakeIncomeRepository()
    service = IncomeService(repository, FakeCategoryRepository())
    service.create_income(
        IncomeCreateSchema(
            amount=1000,
            source="Salary",
            income_date=date(2026, 6, 15),
            category_id=1,
            description="Monthly salary",
            is_recurring=True,
        )
    )
    service.generate_recurring_incomes_for_month(2026, 7)

    created_again = service.generate_recurring_incomes_for_month(2026, 7)

    assert created_again == []
