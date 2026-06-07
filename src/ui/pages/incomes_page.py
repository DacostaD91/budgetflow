import pandas as pd
import streamlit as st

from src.core.exceptions import BudgetFlowException
from src.core.service_factory import get_category_service, get_income_service
from src.schemas.income_schema import IncomeCreateSchema
from src.ui.components.tables import render_dataframe_table


def render_incomes_page() -> None:
    st.title("Incomes")
    income_service = get_income_service()
    category_service = get_category_service()
    categories = category_service.get_income_categories()
    category_options = {category.name: category.id for category in categories}

    with st.form("income_form"):
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        source = st.text_input("Source")
        income_date = st.date_input("Income date")
        category_name = st.selectbox("Category", [""] + list(category_options.keys()))
        description = st.text_area("Description")
        is_recurring = st.checkbox("Recurring income")
        submitted = st.form_submit_button("Add income")

    if submitted:
        try:
            income_service.create_income(
                IncomeCreateSchema(
                    amount=amount,
                    source=source,
                    income_date=income_date,
                    category_id=category_options.get(category_name),
                    description=description or None,
                    is_recurring=is_recurring,
                )
            )
            st.success("Income added successfully.")
        except BudgetFlowException as exc:
            st.error(str(exc))

    _render_incomes_table(income_service.get_all_incomes())


def _render_incomes_table(incomes) -> None:
    data = [
        {
            "Date": income.income_date,
            "Source": income.source,
            "Category": income.category.name if income.category else "",
            "Amount": income.amount,
            "Recurring": income.is_recurring,
            "Description": income.description,
        }
        for income in incomes
    ]
    render_dataframe_table(pd.DataFrame(data))
