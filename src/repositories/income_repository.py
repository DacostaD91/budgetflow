from datetime import date

from src.models.income import Income
from src.repositories.base_repository import BaseRepository


class IncomeRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session, Income)

    def get_by_month(self, year: int, month: int):
        start_date = date(year, month, 1)
        end_date = _next_month_date(year, month)
        return (
            self.db.query(Income)
            .filter(Income.income_date >= start_date)
            .filter(Income.income_date < end_date)
            .all()
        )


def _next_month_date(year: int, month: int) -> date:
    if month == 12:
        return date(year + 1, 1, 1)
    return date(year, month + 1, 1)
