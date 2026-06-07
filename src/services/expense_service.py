from src.core.exceptions import ValidationException
from src.models.expense import Expense
from src.repositories.category_repository import CategoryRepository
from src.repositories.expense_repository import ExpenseRepository
from src.schemas.expense_schema import ExpenseCreateSchema
from src.utils.validators import validate_positive_amount


class ExpenseService:
    def __init__(
        self,
        expense_repository: ExpenseRepository,
        category_repository: CategoryRepository,
    ):
        self.expense_repository = expense_repository
        self.category_repository = category_repository

    def create_expense(self, expense_data: ExpenseCreateSchema) -> Expense:
        validate_positive_amount(expense_data.amount)

        if not expense_data.category_id:
            raise ValidationException("Category is required.")

        if expense_data.expense_date is None:
            raise ValidationException("Expense date is required.")

        if not self.category_repository.get_by_id(expense_data.category_id):
            raise ValidationException("Category does not exist.")

        expense = Expense(
            amount=expense_data.amount,
            category_id=expense_data.category_id,
            expense_date=expense_data.expense_date,
            payment_method=expense_data.payment_method,
            description=expense_data.description,
            is_recurring=expense_data.is_recurring,
        )
        return self.expense_repository.create(expense)

    def get_all_expenses(self):
        return self.expense_repository.get_all()

    def get_monthly_expenses(self, year: int, month: int):
        return self.expense_repository.get_by_month(year, month)

    def get_monthly_expense_total(self, year: int, month: int) -> float:
        return sum(expense.amount for expense in self.get_monthly_expenses(year, month))

    def get_expenses_by_category(self, category_id: int):
        return self.expense_repository.get_by_category(category_id)
