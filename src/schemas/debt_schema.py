from dataclasses import dataclass
from datetime import date


@dataclass
class DebtCreateSchema:
    name: str
    lender: str
    original_amount: float
    current_balance: float
    interest_rate: float | None = None
    monthly_payment: float | None = None
    payment_day: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    notes: str | None = None


@dataclass
class DebtUpdateSchema:
    name: str | None = None
    lender: str | None = None
    current_balance: float | None = None
    interest_rate: float | None = None
    monthly_payment: float | None = None
    payment_day: int | None = None
    end_date: date | None = None
    status: str | None = None
    notes: str | None = None


@dataclass
class DebtPaymentCreateSchema:
    debt_id: int
    amount: float
    payment_date: date
    payment_type: str
    description: str | None = None
