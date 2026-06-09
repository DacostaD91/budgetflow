def calculate_budget_difference(planned_amount: float, actual_amount: float) -> float:
    return planned_amount - actual_amount


def calculate_budget_usage_percentage(planned_amount: float, actual_amount: float) -> float:
    if planned_amount == 0:
        return 0
    return (actual_amount / planned_amount) * 100


def get_budget_status(usage_percentage: float) -> str:
    if usage_percentage <= 70:
        return "Saludable"
    if usage_percentage <= 90:
        return "Cuidado"
    if usage_percentage <= 100:
        return "Cerca del limite"
    return "Sobrepresupuesto"
