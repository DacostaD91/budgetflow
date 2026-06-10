from src.models.debt import Debt
from src.repositories.base_repository import BaseRepository


class DebtRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session, Debt)

    def get_active_debts(self):
        return self.db.query(Debt).filter(Debt.status == "active").all()

    def get_paid_debts(self):
        return self.db.query(Debt).filter(Debt.status == "paid").all()

    def update(self, debt: Debt):
        self.commit()
        self.db.refresh(debt)
        return debt
