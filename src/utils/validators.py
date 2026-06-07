from src.core.exceptions import ValidationException


def validate_positive_amount(amount: float) -> None:
    if amount <= 0:
        raise ValidationException("Amount must be greater than zero.")


def validate_required_text(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValidationException(f"{field_name} is required.")
