import pandas as pd
import streamlit as st

from src.core.exceptions import BudgetFlowException
from src.core.service_factory import get_category_service, get_expense_service
from src.schemas.expense_schema import ExpenseCreateSchema
from src.ui.components.tables import render_dataframe_table


def render_expenses_page() -> None:
    st.title("Expenses")
    expense_service = get_expense_service()
    category_service = get_category_service()
    categories = category_service.get_expense_categories()
    category_options = {category.name: category.id for category in categories}

    with st.form("expense_form"):
        amount = st.number_input("Amount", min_value=0.0, step=100.0)
        category_name = st.selectbox("Category", [""] + list(category_options.keys()))
        expense_date = st.date_input("Expense date")
        payment_method = st.text_input("Payment method")
        description = st.text_area("Description")
        is_recurring = st.checkbox("Recurring expense")
        submitted = st.form_submit_button("Add expense")

    if submitted:
        try:
            expense_service.create_expense(
                ExpenseCreateSchema(
                    amount=amount,
                    category_id=category_options.get(category_name),
                    expense_date=expense_date,
                    payment_method=payment_method or None,
                    description=description or None,
                    is_recurring=is_recurring,
                )
            )
            st.success("Expense added successfully.")
        except BudgetFlowException as exc:
            st.error(str(exc))

    _render_expenses_table(expense_service.get_all_expenses())


def _render_expenses_table(expenses) -> None:
    data = [
        {
            "Date": expense.expense_date,
            "Category": expense.category.name if expense.category else "",
            "Payment Method": expense.payment_method,
            "Amount": expense.amount,
            "Recurring": expense.is_recurring,
            "Description": expense.description,
        }
        for expense in expenses
    ]
    render_dataframe_table(pd.DataFrame(data))
