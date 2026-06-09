from calendar import monthrange
from datetime import date

from src.core.exceptions import NotFoundException, ValidationException
from src.models.income import Income
from src.repositories.category_repository import CategoryRepository
from src.repositories.income_repository import IncomeRepository
from src.schemas.income_schema import IncomeCreateSchema
from src.utils.validators import validate_positive_amount, validate_required_text


class IncomeService:
    def __init__(
        self,
        income_repository: IncomeRepository,
        category_repository: CategoryRepository,
    ):
        self.income_repository = income_repository
        self.category_repository = category_repository

    def create_income(self, income_data: IncomeCreateSchema) -> Income:
        self._validate_income_data(income_data)

        income = Income(
            amount=income_data.amount,
            source=income_data.source.strip(),
            income_date=income_data.income_date,
            category_id=income_data.category_id,
            description=income_data.description,
            is_recurring=income_data.is_recurring,
        )
        return self.income_repository.create(income)

    def update_income(self, income_id: int, income_data: IncomeCreateSchema) -> Income:
        income = self.income_repository.get_by_id(income_id)
        if not income:
            raise NotFoundException("Income not found.")

        self._validate_income_data(income_data)

        income.amount = income_data.amount
        income.source = income_data.source.strip()
        income.income_date = income_data.income_date
        income.category_id = income_data.category_id
        income.description = income_data.description
        income.is_recurring = income_data.is_recurring
        self.income_repository.commit()
        return income

    def get_all_incomes(self):
        return self.income_repository.get_all()

    def get_monthly_incomes(self, year: int, month: int):
        return self.income_repository.get_by_month(year, month)

    def get_monthly_income_total(self, year: int, month: int) -> float:
        return sum(income.amount for income in self.get_monthly_incomes(year, month))

    def generate_recurring_incomes_for_month(self, year: int, month: int) -> list[Income]:
        self._validate_period(year, month)
        templates = self._get_latest_recurring_income_templates(year, month)
        existing_signatures = {
            self._income_signature(income)
            for income in self.income_repository.get_by_month(year, month)
            if income.is_recurring
        }

        created_incomes = []
        for template in templates:
            signature = self._income_signature(template)
            if signature in existing_signatures:
                continue

            created_income = self.create_income(
                IncomeCreateSchema(
                    amount=template.amount,
                    source=template.source,
                    income_date=self._build_target_date(template.income_date, year, month),
                    category_id=template.category_id,
                    description=template.description,
                    is_recurring=True,
                )
            )
            created_incomes.append(created_income)
            existing_signatures.add(signature)

        return created_incomes

    def _validate_income_data(self, income_data: IncomeCreateSchema) -> None:
        validate_positive_amount(income_data.amount)
        validate_required_text(income_data.source, "Source")

        if income_data.income_date is None:
            raise ValidationException("Income date is required.")

        if income_data.category_id and not self.category_repository.get_by_id(income_data.category_id):
            raise ValidationException("Category does not exist.")

    def _validate_period(self, year: int, month: int) -> None:
        if year < 1:
            raise ValidationException("Year must be valid.")
        if month < 1 or month > 12:
            raise ValidationException("Month must be between 1 and 12.")

    def _get_latest_recurring_income_templates(self, year: int, month: int):
        templates_by_signature = {}
        for income in self.income_repository.get_recurring_before_month(year, month):
            signature = self._income_signature(income)
            if signature not in templates_by_signature:
                templates_by_signature[signature] = income
        return list(templates_by_signature.values())

    def _income_signature(self, income) -> tuple:
        return (
            income.source,
            income.category_id,
            income.amount,
            income.description,
        )

    def _build_target_date(self, source_date: date, year: int, month: int) -> date:
        last_day = monthrange(year, month)[1]
        return date(year, month, min(source_date.day, last_day))
