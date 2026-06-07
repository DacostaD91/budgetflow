def build_monthly_summary(total_income: float, total_expenses: float) -> dict:
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": total_income - total_expenses,
    }
