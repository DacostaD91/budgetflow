from dataclasses import dataclass
from datetime import date


@dataclass
class ExpenseCreateSchema:
    amount: float
    category_id: int
    expense_date: date
    payment_method: str | None = None
    description: str | None = None
    is_recurring: bool = False
