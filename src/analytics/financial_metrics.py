def calculate_net_balance(total_income: float, total_expenses: float) -> float:
    return total_income - total_expenses


def calculate_percentage(part: float, total: float) -> float:
    if total == 0:
        return 0
    return (part / total) * 100
