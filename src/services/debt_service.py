from src.analytics.debt_analysis import (
    calculate_debt_progress,
    calculate_remaining_balance_after_payment,
    calculate_total_debt_balance,
    calculate_total_monthly_payment,
)
from src.core.exceptions import NotFoundException, ValidationException
from src.models.debt import Debt
from src.models.debt_payment import DebtPayment
from src.repositories.debt_payment_repository import DebtPaymentRepository
from src.repositories.debt_repository import DebtRepository
from src.schemas.debt_schema import DebtCreateSchema, DebtPaymentCreateSchema, DebtUpdateSchema
from src.utils.validators import validate_positive_amount, validate_required_text

VALID_DEBT_STATUSES = {"active", "paid"}
VALID_PAYMENT_TYPES = {"regular", "extra_principal"}


class DebtService:
    def __init__(
        self,
        debt_repository: DebtRepository,
        debt_payment_repository: DebtPaymentRepository,
    ):
        self.debt_repository = debt_repository
        self.debt_payment_repository = debt_payment_repository

    def create_debt(self, debt_data: DebtCreateSchema) -> Debt:
        self._validate_debt_create_data(debt_data)
        status = "paid" if debt_data.current_balance == 0 else "active"
        debt = Debt(
            name=debt_data.name.strip(),
            lender=debt_data.lender.strip(),
            original_amount=debt_data.original_amount,
            current_balance=debt_data.current_balance,
            interest_rate=debt_data.interest_rate,
            monthly_payment=debt_data.monthly_payment,
            payment_day=debt_data.payment_day,
            start_date=debt_data.start_date,
            end_date=debt_data.end_date,
            status=status,
            notes=debt_data.notes,
        )
        return self.debt_repository.create(debt)

    def update_debt(self, debt_id: int, debt_data: DebtUpdateSchema) -> Debt:
        debt = self.debt_repository.get_by_id(debt_id)
        if not debt:
            raise NotFoundException("Debt not found.")

        self._validate_debt_update_data(debt, debt_data)

        if debt_data.name is not None:
            validate_required_text(debt_data.name, "Debt name")
            debt.name = debt_data.name.strip()
        if debt_data.lender is not None:
            validate_required_text(debt_data.lender, "Lender")
            debt.lender = debt_data.lender.strip()
        if debt_data.current_balance is not None:
            debt.current_balance = debt_data.current_balance
        if debt_data.interest_rate is not None:
            debt.interest_rate = debt_data.interest_rate
        if debt_data.monthly_payment is not None:
            debt.monthly_payment = debt_data.monthly_payment
        if debt_data.payment_day is not None:
            debt.payment_day = debt_data.payment_day
        if debt_data.end_date is not None:
            debt.end_date = debt_data.end_date
        if debt_data.notes is not None:
            debt.notes = debt_data.notes

        if debt.current_balance == 0:
            debt.status = "paid"
        elif debt_data.status is not None:
            debt.status = debt_data.status
        elif debt.status == "paid":
            debt.status = "active"

        return self.debt_repository.update(debt)

    def delete_debt(self, debt_id: int) -> None:
        debt = self.debt_repository.get_by_id(debt_id)
        if not debt:
            raise NotFoundException("Debt not found.")
        self.debt_repository.delete(debt)

    def get_all_debts(self):
        return self.debt_repository.get_all()

    def get_active_debts(self):
        return self.debt_repository.get_active_debts()

    def get_paid_debts(self):
        return self.debt_repository.get_paid_debts()

    def get_debt_details(self, debt_id: int) -> dict:
        debt = self.debt_repository.get_by_id(debt_id)
        if not debt:
            raise NotFoundException("Debt not found.")
        payments = self.debt_payment_repository.get_by_debt(debt_id)
        return {
            "debt": debt,
            "payments": payments,
            "progress": self.get_debt_progress(debt_id),
            "remaining_balance": debt.current_balance,
            "status": debt.status,
        }

    def register_payment(self, payment_data: DebtPaymentCreateSchema) -> DebtPayment:
        debt = self.debt_repository.get_by_id(payment_data.debt_id)
        if not debt:
            raise ValidationException("Debt does not exist.")
        if debt.status == "paid":
            raise ValidationException("Cannot register payments for a paid debt.")

        self._validate_payment_data(payment_data)
        payment = DebtPayment(
            debt_id=payment_data.debt_id,
            amount=payment_data.amount,
            payment_date=payment_data.payment_date,
            payment_type=payment_data.payment_type,
            description=payment_data.description,
        )
        created_payment = self.debt_payment_repository.create(payment)

        debt.current_balance = calculate_remaining_balance_after_payment(debt.current_balance, payment_data.amount)
        debt.status = "paid" if debt.current_balance == 0 else "active"
        self.debt_repository.update(debt)
        return created_payment

    def get_payments_by_debt(self, debt_id: int):
        debt = self.debt_repository.get_by_id(debt_id)
        if not debt:
            raise NotFoundException("Debt not found.")
        return self.debt_payment_repository.get_by_debt(debt_id)

    def get_total_debt_balance(self) -> float:
        return calculate_total_debt_balance(self.get_all_debts())

    def get_total_monthly_debt_payment(self) -> float:
        return calculate_total_monthly_payment(self.get_active_debts())

    def get_debt_progress(self, debt_id: int) -> float:
        debt = self.debt_repository.get_by_id(debt_id)
        if not debt:
            raise NotFoundException("Debt not found.")
        return calculate_debt_progress(debt.original_amount, debt.current_balance)

    def get_debt_summary(self) -> dict:
        debts = self.get_all_debts()
        if not debts:
            return {
                "total_debt_balance": 0,
                "total_monthly_payment": 0,
                "active_debts": 0,
                "paid_debts": 0,
                "highest_debt_name": None,
                "highest_debt_balance": 0,
                "average_progress": 0,
            }

        active_debts = [debt for debt in debts if debt.status == "active"]
        paid_debts = [debt for debt in debts if debt.status == "paid"]
        highest_debt = max(debts, key=lambda debt: debt.current_balance)
        average_progress = sum(
            calculate_debt_progress(debt.original_amount, debt.current_balance) for debt in debts
        ) / len(debts)

        return {
            "total_debt_balance": calculate_total_debt_balance(debts),
            "total_monthly_payment": calculate_total_monthly_payment(active_debts),
            "active_debts": len(active_debts),
            "paid_debts": len(paid_debts),
            "highest_debt_name": highest_debt.name,
            "highest_debt_balance": highest_debt.current_balance,
            "average_progress": average_progress,
        }

    def mark_debt_as_paid(self, debt_id: int) -> Debt:
        debt = self.debt_repository.get_by_id(debt_id)
        if not debt:
            raise NotFoundException("Debt not found.")
        debt.current_balance = 0
        debt.status = "paid"
        return self.debt_repository.update(debt)

    def _validate_debt_create_data(self, debt_data: DebtCreateSchema) -> None:
        validate_required_text(debt_data.name, "Debt name")
        validate_required_text(debt_data.lender, "Lender")
        validate_positive_amount(debt_data.original_amount)
        self._validate_balance(debt_data.current_balance, debt_data.original_amount)
        self._validate_optional_numbers(debt_data.interest_rate, debt_data.monthly_payment, debt_data.payment_day)

    def _validate_debt_update_data(self, debt: Debt, debt_data: DebtUpdateSchema) -> None:
        if debt_data.current_balance is not None:
            self._validate_balance(debt_data.current_balance, debt.original_amount)
        self._validate_optional_numbers(debt_data.interest_rate, debt_data.monthly_payment, debt_data.payment_day)
        if debt_data.status is not None and debt_data.status not in VALID_DEBT_STATUSES:
            raise ValidationException("Debt status is invalid.")

    def _validate_balance(self, current_balance: float, original_amount: float) -> None:
        if current_balance < 0:
            raise ValidationException("Current balance cannot be negative.")
        if current_balance > original_amount:
            raise ValidationException("Current balance cannot be greater than original amount.")

    def _validate_optional_numbers(
        self,
        interest_rate: float | None,
        monthly_payment: float | None,
        payment_day: int | None,
    ) -> None:
        if interest_rate is not None and interest_rate < 0:
            raise ValidationException("Interest rate cannot be negative.")
        if monthly_payment is not None and monthly_payment < 0:
            raise ValidationException("Monthly payment cannot be negative.")
        if payment_day is not None and (payment_day < 1 or payment_day > 31):
            raise ValidationException("Payment day must be between 1 and 31.")

    def _validate_payment_data(self, payment_data: DebtPaymentCreateSchema) -> None:
        validate_positive_amount(payment_data.amount)
        if payment_data.payment_date is None:
            raise ValidationException("Payment date is required.")
        if payment_data.payment_type not in VALID_PAYMENT_TYPES:
            raise ValidationException("Payment type is invalid.")
