from src.analytics.cashflow_analysis import build_monthly_summary
from src.repositories.expense_repository import ExpenseRepository
from src.repositories.income_repository import IncomeRepository


class ReportService:
    def __init__(
        self,
        income_repository: IncomeRepository,
        expense_repository: ExpenseRepository,
    ):
        self.income_repository = income_repository
        self.expense_repository = expense_repository

    def get_monthly_summary(self, year: int, month: int) -> dict:
        total_income = sum(income.amount for income in self.income_repository.get_by_month(year, month))
        total_expenses = sum(expense.amount for expense in self.expense_repository.get_by_month(year, month))
        return build_monthly_summary(total_income, total_expenses)

    def get_expenses_by_category_summary(self, year: int, month: int) -> list[dict]:
        expenses = self.expense_repository.get_by_month(year, month)
        summary: dict[str, float] = {}

        for expense in expenses:
            category_name = expense.category.name if expense.category else "Uncategorized"
            summary[category_name] = summary.get(category_name, 0) + expense.amount

        return [{"category": category, "amount": amount} for category, amount in summary.items()]

    def get_cashflow_summary(self, year: int, month: int) -> dict:
        return self.get_monthly_summary(year, month)
