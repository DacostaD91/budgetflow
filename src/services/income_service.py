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

    def _validate_income_data(self, income_data: IncomeCreateSchema) -> None:
        validate_positive_amount(income_data.amount)
        validate_required_text(income_data.source, "Source")

        if income_data.income_date is None:
            raise ValidationException("Income date is required.")

        if income_data.category_id and not self.category_repository.get_by_id(income_data.category_id):
            raise ValidationException("Category does not exist.")
