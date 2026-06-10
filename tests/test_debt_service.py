from dataclasses import dataclass, field
from datetime import date

import pytest

from src.core.exceptions import ValidationException
from src.schemas.debt_schema import DebtCreateSchema, DebtPaymentCreateSchema
from src.services.debt_service import DebtService


@dataclass
class FakeDebt:
    id: int
    name: str
    lender: str
    original_amount: float
    current_balance: float
    interest_rate: float | None = None
    monthly_payment: float | None = None
    payment_day: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str = "active"
    notes: str | None = None
    payments: list = field(default_factory=list)


@dataclass
class FakeDebtPayment:
    id: int
    debt_id: int
    amount: float
    payment_date: date
    payment_type: str
    description: str | None = None
    debt: FakeDebt | None = None


class FakeDebtRepository:
    def __init__(self):
        self.debts = []
        self.next_id = 1

    def create(self, debt):
        fake_debt = FakeDebt(
            id=self.next_id,
            name=debt.name,
            lender=debt.lender,
            original_amount=debt.original_amount,
            current_balance=debt.current_balance,
            interest_rate=debt.interest_rate,
            monthly_payment=debt.monthly_payment,
            payment_day=debt.payment_day,
            start_date=debt.start_date,
            end_date=debt.end_date,
            status=debt.status,
            notes=debt.notes,
        )
        self.next_id += 1
        self.debts.append(fake_debt)
        return fake_debt

    def get_all(self):
        return self.debts

    def get_by_id(self, debt_id):
        return next((debt for debt in self.debts if debt.id == debt_id), None)

    def get_active_debts(self):
        return [debt for debt in self.debts if debt.status == "active"]

    def get_paid_debts(self):
        return [debt for debt in self.debts if debt.status == "paid"]

    def update(self, debt):
        return debt

    def delete(self, debt):
        self.debts.remove(debt)


class FakeDebtPaymentRepository:
    def __init__(self, debt_repository):
        self.debt_repository = debt_repository
        self.payments = []
        self.next_id = 1

    def create(self, payment):
        debt = self.debt_repository.get_by_id(payment.debt_id)
        fake_payment = FakeDebtPayment(
            id=self.next_id,
            debt_id=payment.debt_id,
            amount=payment.amount,
            payment_date=payment.payment_date,
            payment_type=payment.payment_type,
            description=payment.description,
            debt=debt,
        )
        self.next_id += 1
        self.payments.append(fake_payment)
        if debt:
            debt.payments.append(fake_payment)
        return fake_payment

    def get_by_debt(self, debt_id):
        return [payment for payment in self.payments if payment.debt_id == debt_id]


def build_service():
    debt_repository = FakeDebtRepository()
    payment_repository = FakeDebtPaymentRepository(debt_repository)
    return DebtService(debt_repository, payment_repository), debt_repository, payment_repository


def valid_debt_data(**overrides):
    data = {
        "name": "BHD Loan",
        "lender": "Banco BHD",
        "original_amount": 1000,
        "current_balance": 1000,
        "interest_rate": 12,
        "monthly_payment": 100,
        "payment_day": 15,
    }
    data.update(overrides)
    return DebtCreateSchema(**data)


def test_create_debt_requires_name():
    service, _, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_debt(valid_debt_data(name=""))


def test_create_debt_requires_lender():
    service, _, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_debt(valid_debt_data(lender=""))


def test_create_debt_requires_positive_original_amount():
    service, _, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_debt(valid_debt_data(original_amount=0))


def test_create_debt_rejects_negative_current_balance():
    service, _, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_debt(valid_debt_data(current_balance=-1))


def test_create_debt_rejects_balance_greater_than_original_amount():
    service, _, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_debt(valid_debt_data(current_balance=1200))


def test_create_debt_rejects_negative_interest_rate():
    service, _, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_debt(valid_debt_data(interest_rate=-1))


def test_create_debt_rejects_payment_day_less_than_one():
    service, _, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_debt(valid_debt_data(payment_day=0))


def test_create_debt_rejects_payment_day_greater_than_thirty_one():
    service, _, _ = build_service()

    with pytest.raises(ValidationException):
        service.create_debt(valid_debt_data(payment_day=32))


def test_create_debt_allows_valid_debt():
    service, _, _ = build_service()

    debt = service.create_debt(valid_debt_data())

    assert debt.name == "BHD Loan"
    assert debt.status == "active"


def test_register_payment_reduces_current_balance():
    service, _, _ = build_service()
    debt = service.create_debt(valid_debt_data())

    service.register_payment(DebtPaymentCreateSchema(debt.id, 300, date.today(), "regular"))

    assert debt.current_balance == 700


def test_register_payment_rejects_non_positive_amount():
    service, _, _ = build_service()
    debt = service.create_debt(valid_debt_data())

    with pytest.raises(ValidationException):
        service.register_payment(DebtPaymentCreateSchema(debt.id, 0, date.today(), "regular"))


def test_register_payment_rejects_missing_debt():
    service, _, _ = build_service()

    with pytest.raises(ValidationException):
        service.register_payment(DebtPaymentCreateSchema(99, 100, date.today(), "regular"))


def test_register_payment_rejects_paid_debt():
    service, _, _ = build_service()
    debt = service.create_debt(valid_debt_data(current_balance=0))

    with pytest.raises(ValidationException):
        service.register_payment(DebtPaymentCreateSchema(debt.id, 100, date.today(), "regular"))


def test_register_payment_marks_debt_as_paid_when_balance_reaches_zero():
    service, _, _ = build_service()
    debt = service.create_debt(valid_debt_data())

    service.register_payment(DebtPaymentCreateSchema(debt.id, 1000, date.today(), "regular"))

    assert debt.current_balance == 0
    assert debt.status == "paid"


def test_register_payment_never_leaves_negative_balance():
    service, _, _ = build_service()
    debt = service.create_debt(valid_debt_data())

    service.register_payment(DebtPaymentCreateSchema(debt.id, 1200, date.today(), "extra_principal"))

    assert debt.current_balance == 0


def test_get_debt_summary_calculates_totals():
    service, _, _ = build_service()
    service.create_debt(valid_debt_data(name="BHD", current_balance=700, monthly_payment=100))
    service.create_debt(valid_debt_data(name="Card", current_balance=0, monthly_payment=200))

    summary = service.get_debt_summary()

    assert summary["total_debt_balance"] == 700
    assert summary["total_monthly_payment"] == 100
    assert summary["active_debts"] == 1
    assert summary["paid_debts"] == 1
    assert summary["highest_debt_name"] == "BHD"
