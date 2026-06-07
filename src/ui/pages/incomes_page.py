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

    _render_incomes_table(income_service.get_all_incomes(), income_service, category_options)


def _render_incomes_table(incomes, income_service, category_options: dict[str, int]) -> None:
    data = [
        {
            "ID": income.id,
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

    if not incomes:
        return

    st.subheader("Edit Income")
    for income in incomes:
        label = f"{income.income_date} - {income.source} - {income.amount:,.2f}"
        with st.expander(label):
            if st.button("Edit", key=f"edit_income_{income.id}"):
                st.session_state["editing_income_id"] = income.id

            if st.session_state.get("editing_income_id") == income.id:
                _render_income_edit_form(income, income_service, category_options)


def _render_income_edit_form(income, income_service, category_options: dict[str, int]) -> None:
    category_names = [""] + list(category_options.keys())
    current_category = income.category.name if income.category else ""
    current_index = category_names.index(current_category) if current_category in category_names else 0

    with st.form(f"edit_income_form_{income.id}"):
        amount = st.number_input("Amount", min_value=0.0, step=100.0, value=float(income.amount), key=f"income_amount_{income.id}")
        source = st.text_input("Source", value=income.source, key=f"income_source_{income.id}")
        income_date = st.date_input("Income date", value=income.income_date, key=f"income_date_{income.id}")
        category_name = st.selectbox("Category", category_names, index=current_index, key=f"income_category_{income.id}")
        description = st.text_area("Description", value=income.description or "", key=f"income_description_{income.id}")
        is_recurring = st.checkbox("Recurring income", value=income.is_recurring, key=f"income_recurring_{income.id}")
        col_save, col_cancel = st.columns(2)
        with col_save:
            save = st.form_submit_button("Save changes")
        with col_cancel:
            cancel = st.form_submit_button("Cancel")

    if cancel:
        st.session_state.pop("editing_income_id", None)
        st.rerun()

    if save:
        try:
            income_service.update_income(
                income.id,
                IncomeCreateSchema(
                    amount=amount,
                    source=source,
                    income_date=income_date,
                    category_id=category_options.get(category_name),
                    description=description or None,
                    is_recurring=is_recurring,
                ),
            )
            st.session_state.pop("editing_income_id", None)
            st.success("Income updated successfully.")
            st.rerun()
        except BudgetFlowException as exc:
            st.error(str(exc))
