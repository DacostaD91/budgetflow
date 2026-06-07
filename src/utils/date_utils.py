from datetime import date


def get_current_year_month() -> tuple[int, int]:
    today = date.today()
    return today.year, today.month
