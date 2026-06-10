from datetime import date

from src.models.debt_payment import DebtPayment
from src.repositories.base_repository import BaseRepository


class DebtPaymentRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session, DebtPayment)

    def get_by_debt(self, debt_id: int):
        return (
            self.db.query(DebtPayment)
            .filter(DebtPayment.debt_id == debt_id)
            .order_by(DebtPayment.payment_date.desc())
            .all()
        )

    def get_by_month(self, year: int, month: int):
        start_date = date(year, month, 1)
        end_date = _next_month_date(year, month)
        return (
            self.db.query(DebtPayment)
            .filter(DebtPayment.payment_date >= start_date)
            .filter(DebtPayment.payment_date < end_date)
            .all()
        )


def _next_month_date(year: int, month: int) -> date:
    if month == 12:
        return date(year + 1, 1, 1)
    return date(year, month + 1, 1)
