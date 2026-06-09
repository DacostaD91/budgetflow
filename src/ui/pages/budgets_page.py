import streamlit as st

from src.core.exceptions import BudgetFlowException
from src.core.service_factory import get_budget_service, get_category_service
from src.schemas.budget_schema import MonthlyBudgetCreateSchema, MonthlyBudgetUpdateSchema
from src.ui.components.charts import render_budget_usage_chart, render_budget_vs_actual_chart
from src.ui.components.metrics import render_budget_summary_metrics
from src.ui.components.tables import render_budget_vs_actual_table
from src.utils.date_utils import get_current_year_month


def render_budgets_page() -> None:
    st.title("Budgets")
    budget_service = get_budget_service()
    category_service = get_category_service()
    category_options = _get_expense_category_options(category_service)

    selected_year, selected_month = _render_period_selector()
    _render_budget_form(budget_service, category_options, selected_year, selected_month)

    summary = budget_service.get_monthly_budget_summary(selected_year, selected_month)
    budget_vs_actual = budget_service.get_budget_vs_actual(selected_year, selected_month)

    st.subheader("Monthly Summary")
    render_budget_summary_metrics(summary)

    st.subheader("Budget vs Actual")
    _render_budget_table(budget_vs_actual, budget_service)

    st.subheader("Charts")
    tab_comparison, tab_usage = st.tabs(["Planned vs Actual", "Usage"])
    with tab_comparison:
        render_budget_vs_actual_chart(budget_vs_actual)
    with tab_usage:
        render_budget_usage_chart(budget_vs_actual)


def _render_period_selector() -> tuple[int, int]:
    current_year, current_month = get_current_year_month()
    col_year, col_month = st.columns(2)
    with col_year:
        selected_year = st.number_input("Year", min_value=2000, max_value=2100, value=current_year, step=1)
    with col_month:
        selected_month = st.selectbox(
            "Month",
            list(range(1, 13)),
            index=current_month - 1,
            format_func=lambda month: f"{month:02d}",
        )
    return int(selected_year), int(selected_month)


def _render_budget_form(
    budget_service,
    category_options: dict[str, int],
    selected_year: int,
    selected_month: int,
) -> None:
    st.subheader("Create Monthly Budget")

    with st.form("budget_form"):
        category_name = st.selectbox("Expense category", [""] + list(category_options.keys()))
        planned_amount = st.number_input("Planned amount", min_value=0.0, step=500.0)
        submitted = st.form_submit_button("Add budget")

    if submitted:
        try:
            budget_service.create_monthly_budget(
                MonthlyBudgetCreateSchema(
                    year=selected_year,
                    month=selected_month,
                    category_id=category_options.get(category_name),
                    planned_amount=planned_amount,
                )
            )
            st.success("Budget added successfully.")
            st.rerun()
        except BudgetFlowException as exc:
            st.error(str(exc))


def _render_budget_table(budget_vs_actual: list[dict], budget_service) -> None:
    for item, action_col in render_budget_vs_actual_table(budget_vs_actual):
        edit_col, delete_col = action_col.columns(2)
        if edit_col.button("Edit", key=f"edit_budget_{item['budget_id']}"):
            _render_edit_budget_dialog(item, budget_service)
        if delete_col.button("Delete", key=f"delete_budget_{item['budget_id']}"):
            _render_delete_budget_dialog(item, budget_service)


@st.dialog("Edit Budget")
def _render_edit_budget_dialog(item: dict, budget_service) -> None:
    with st.form(f"edit_budget_form_{item['budget_id']}"):
        planned_amount = st.number_input(
            "Planned amount",
            min_value=0.0,
            step=500.0,
            value=float(item["planned_amount"]),
        )
        col_save, col_cancel = st.columns(2)
        with col_save:
            save = st.form_submit_button("Save changes")
        with col_cancel:
            cancel = st.form_submit_button("Cancel")

    if cancel:
        st.rerun()

    if save:
        try:
            budget_service.update_monthly_budget(
                item["budget_id"],
                MonthlyBudgetUpdateSchema(planned_amount=planned_amount),
            )
            st.success("Budget updated successfully.")
            st.rerun()
        except BudgetFlowException as exc:
            st.error(str(exc))


@st.dialog("Delete Budget")
def _render_delete_budget_dialog(item: dict, budget_service) -> None:
    st.write(f"Delete the budget for {item['category_name']}?")
    col_delete, col_cancel = st.columns(2)
    if col_delete.button("Delete budget", type="primary"):
        try:
            budget_service.delete_monthly_budget(item["budget_id"])
            st.success("Budget deleted successfully.")
            st.rerun()
        except BudgetFlowException as exc:
            st.error(str(exc))
    if col_cancel.button("Cancel"):
        st.rerun()


def _get_expense_category_options(category_service) -> dict[str, int]:
    categories = category_service.get_expense_categories()
    return {category.name: category.id for category in categories}
