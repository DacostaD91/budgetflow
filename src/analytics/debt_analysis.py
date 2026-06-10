def calculate_debt_progress(original_amount: float, current_balance: float) -> float:
    if original_amount <= 0:
        return 0

    paid_amount = original_amount - current_balance
    return (paid_amount / original_amount) * 100


def calculate_remaining_balance_after_payment(current_balance: float, payment_amount: float) -> float:
    new_balance = current_balance - payment_amount
    return max(new_balance, 0)


def calculate_total_debt_balance(debts: list) -> float:
    return sum(debt.current_balance for debt in debts)


def calculate_total_monthly_payment(debts: list) -> float:
    return sum(debt.monthly_payment or 0 for debt in debts)
