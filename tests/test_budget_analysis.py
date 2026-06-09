from src.analytics.budget_analysis import (
    calculate_budget_difference,
    calculate_budget_usage_percentage,
    get_budget_status,
)


def test_calculate_budget_difference_with_remaining_amount():
    assert calculate_budget_difference(1000, 500) == 500


def test_calculate_budget_difference_with_overbudget_amount():
    assert calculate_budget_difference(1000, 1200) == -200


def test_calculate_budget_usage_percentage():
    assert calculate_budget_usage_percentage(1000, 800) == 80


def test_calculate_budget_usage_percentage_returns_zero_when_planned_is_zero():
    assert calculate_budget_usage_percentage(0, 500) == 0


def test_get_budget_status():
    assert get_budget_status(50) == "Saludable"
    assert get_budget_status(80) == "Cuidado"
    assert get_budget_status(95) == "Cerca del limite"
    assert get_budget_status(120) == "Sobrepresupuesto"
