from src.analytics.debt_analysis import (
    calculate_debt_progress,
    calculate_remaining_balance_after_payment,
    calculate_total_debt_balance,
    calculate_total_monthly_payment,
)


class FakeDebt:
    def __init__(self, current_balance, monthly_payment=None):
        self.current_balance = current_balance
        self.monthly_payment = monthly_payment


def test_calculate_debt_progress():
    assert calculate_debt_progress(1000, 500) == 50
    assert calculate_debt_progress(1000, 0) == 100
    assert calculate_debt_progress(1000, 1000) == 0
    assert calculate_debt_progress(0, 0) == 0


def test_calculate_remaining_balance_after_payment():
    assert calculate_remaining_balance_after_payment(1000, 300) == 700
    assert calculate_remaining_balance_after_payment(1000, 1200) == 0


def test_calculate_total_debt_balance():
    debts = [FakeDebt(1000), FakeDebt(500)]

    assert calculate_total_debt_balance(debts) == 1500


def test_calculate_total_monthly_payment():
    debts = [FakeDebt(1000, 100), FakeDebt(500, None), FakeDebt(300, 50)]

    assert calculate_total_monthly_payment(debts) == 150
