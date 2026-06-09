from dataclasses import dataclass


@dataclass
class MonthlyBudgetCreateSchema:
    year: int
    month: int
    category_id: int
    planned_amount: float


@dataclass
class MonthlyBudgetUpdateSchema:
    planned_amount: float
