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
