from dataclasses import dataclass
from datetime import date


@dataclass
class IncomeCreateSchema:
    amount: float
    source: str
    income_date: date
    category_id: int | None = None
    description: str | None = None
    is_recurring: bool = False
