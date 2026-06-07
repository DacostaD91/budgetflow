def format_currency(amount: float, currency: str = "DOP") -> str:
    return f"{currency} {amount:,.2f}"
