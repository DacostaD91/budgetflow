import streamlit as st

from src.core.service_factory import get_report_service
from src.ui.components.charts import render_expenses_by_category_chart
from src.ui.components.metrics import render_metric_card
from src.utils.date_utils import get_current_year_month
from src.utils.money_utils import format_currency


def render_dashboard_page() -> None:
    st.title("BudgetFlow")
    year, month = get_current_year_month()
    report_service = get_report_service()

    summary = report_service.get_monthly_summary(year, month)
    expenses_by_category = report_service.get_expenses_by_category_summary(year, month)

    col_income, col_expenses, col_balance = st.columns(3)
    with col_income:
        render_metric_card("Total Income", format_currency(summary["total_income"]))
    with col_expenses:
        render_metric_card("Total Expenses", format_currency(summary["total_expenses"]))
    with col_balance:
        render_metric_card("Net Balance", format_currency(summary["net_balance"]))

    st.subheader("Expenses by Category")
    render_expenses_by_category_chart(expenses_by_category)
