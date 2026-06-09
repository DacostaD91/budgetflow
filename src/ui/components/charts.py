import pandas as pd
import plotly.express as px
import streamlit as st


def render_expenses_by_category_chart(data):
    if not data:
        st.info("No expense data available for this month.")
        return

    dataframe = pd.DataFrame(data)
    figure = px.pie(dataframe, names="category", values="amount")
    st.plotly_chart(figure, use_container_width=True)


def render_budget_vs_actual_chart(data):
    if not data:
        st.info("No budget data available for this month.")
        return

    dataframe = pd.DataFrame(data)
    chart_data = dataframe.melt(
        id_vars=["category_name"],
        value_vars=["planned_amount", "actual_amount"],
        var_name="Type",
        value_name="Amount",
    )
    chart_data["Type"] = chart_data["Type"].map(
        {
            "planned_amount": "Planned Amount",
            "actual_amount": "Actual Amount",
        }
    )
    figure = px.bar(chart_data, x="category_name", y="Amount", color="Type", barmode="group")
    figure.update_layout(xaxis_title="Category", yaxis_title="Amount")
    st.plotly_chart(figure, use_container_width=True)


def render_budget_usage_chart(data):
    if not data:
        st.info("No budget usage data available for this month.")
        return

    dataframe = pd.DataFrame(data)
    figure = px.bar(
        dataframe,
        x="category_name",
        y="usage_percentage",
        color="status",
        labels={"category_name": "Category", "usage_percentage": "Usage %", "status": "Status"},
    )
    figure.add_hline(y=100, line_dash="dash", line_color="red")
    st.plotly_chart(figure, use_container_width=True)
