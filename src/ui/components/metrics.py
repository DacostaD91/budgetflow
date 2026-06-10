import streamlit as st


def render_metric_card(label: str, value: str):
    st.metric(label=label, value=value)


def render_budget_summary_metrics(summary: dict) -> None:
    col_planned, col_spent, col_difference, col_usage, col_overbudget = st.columns(5)
    with col_planned:
        st.metric("Total Budgeted", f"DOP {summary['total_planned']:,.2f}")
    with col_spent:
        st.metric("Total Spent", f"DOP {summary['total_actual']:,.2f}")
    with col_difference:
        st.metric("Difference", f"DOP {summary['difference']:,.2f}")
    with col_usage:
        st.metric("Budget Usage", f"{summary['usage_percentage']:.2f}%")
    with col_overbudget:
        st.metric("Overbudget Categories", summary["overbudget_categories"])


def render_debt_summary_metrics(summary: dict) -> None:
    col_balance, col_payment, col_active, col_paid, col_highest, col_progress = st.columns(6)
    with col_balance:
        st.metric("Total Debt Balance", f"DOP {summary['total_debt_balance']:,.2f}")
    with col_payment:
        st.metric("Monthly Payment", f"DOP {summary['total_monthly_payment']:,.2f}")
    with col_active:
        st.metric("Active Debts", summary["active_debts"])
    with col_paid:
        st.metric("Paid Debts", summary["paid_debts"])
    with col_highest:
        st.metric("Highest Debt", summary["highest_debt_name"] or "None")
    with col_progress:
        st.metric("Average Progress", f"{summary['average_progress']:.2f}%")
