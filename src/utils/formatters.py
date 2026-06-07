from src.utils.money_utils import format_currency


def format_optional_text(value: str | None) -> str:
    return value or ""


__all__ = ["format_currency", "format_optional_text"]
