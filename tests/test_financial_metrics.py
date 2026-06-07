from src.analytics.financial_metrics import calculate_net_balance, calculate_percentage


def test_calculate_net_balance():
    assert calculate_net_balance(1000, 250) == 750


def test_calculate_percentage_returns_zero_when_total_is_zero():
    assert calculate_percentage(10, 0) == 0


def test_calculate_percentage():
    assert calculate_percentage(25, 100) == 25
