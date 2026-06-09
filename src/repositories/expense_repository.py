from datetime import date

from src.models.expense import Expense
from src.repositories.base_repository import BaseRepository


class ExpenseRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session, Expense)

    def get_by_month(self, year: int, month: int):
        start_date = date(year, month, 1)
        end_date = _next_month_date(year, month)
        return (
            self.db.query(Expense)
            .filter(Expense.expense_date >= start_date)
            .filter(Expense.expense_date < end_date)
            .all()
        )

    def get_by_category(self, category_id: int):
        return self.db.query(Expense).filter(Expense.category_id == category_id).all()

    def get_recurring_before_month(self, year: int, month: int):
        start_date = date(year, month, 1)
        return (
            self.db.query(Expense)
            .filter(Expense.is_recurring.is_(True))
            .filter(Expense.expense_date < start_date)
            .order_by(Expense.expense_date.desc())
            .all()
        )


def _next_month_date(year: int, month: int) -> date:
    if month == 12:
        return date(year + 1, 1, 1)
    return date(year, month + 1, 1)
