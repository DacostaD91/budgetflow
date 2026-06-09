from src.models.monthly_budget import MonthlyBudget
from src.repositories.base_repository import BaseRepository


class BudgetRepository(BaseRepository):
    def __init__(self, db_session):
        super().__init__(db_session, MonthlyBudget)

    def get_by_month(self, year: int, month: int):
        return (
            self.db.query(MonthlyBudget)
            .filter(MonthlyBudget.year == year)
            .filter(MonthlyBudget.month == month)
            .all()
        )

    def get_by_category_month(self, year: int, month: int, category_id: int):
        return (
            self.db.query(MonthlyBudget)
            .filter(MonthlyBudget.year == year)
            .filter(MonthlyBudget.month == month)
            .filter(MonthlyBudget.category_id == category_id)
            .first()
        )

    def update(self, budget: MonthlyBudget):
        self.commit()
        self.db.refresh(budget)
        return budget
