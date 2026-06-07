import streamlit as st

from src.core.exceptions import BudgetFlowException
from src.core.service_factory import get_category_service, get_expense_service
from src.schemas.expense_schema import ExpenseCreateSchema


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

    _render_expenses_table(expense_service.get_all_expenses(), expense_service, category_options)


def _render_expenses_table(expenses, expense_service, category_options: dict[str, int]) -> None:
    if not expenses:
        st.info("No records found.")
        return

    st.subheader("Expense Records")
    header_cols = st.columns([0.8, 1.3, 1.7, 1.5, 1.2, 1.1, 2.1, 0.8])
    headers = ["ID", "Date", "Category", "Payment", "Amount", "Recurring", "Description", ""]
    for col, header in zip(header_cols, headers):
        col.caption(header)

    for expense in expenses:
        row_cols = st.columns([0.8, 1.3, 1.7, 1.5, 1.2, 1.1, 2.1, 0.8])
        row_cols[0].write(expense.id)
        row_cols[1].write(expense.expense_date)
        row_cols[2].write(expense.category.name if expense.category else "")
        row_cols[3].write(expense.payment_method or "")
        row_cols[4].write(f"{expense.amount:,.2f}")
        row_cols[5].write("Yes" if expense.is_recurring else "No")
        row_cols[6].write(expense.description or "")
        if row_cols[7].button("Edit", key=f"open_expense_modal_{expense.id}"):
            _render_expense_edit_dialog(expense, expense_service, category_options)


@st.dialog("Edit Expense")
def _render_expense_edit_dialog(expense, expense_service, category_options: dict[str, int]) -> None:
    category_names = [""] + list(category_options.keys())
    current_category = expense.category.name if expense.category else ""
    current_index = category_names.index(current_category) if current_category in category_names else 0

    with st.form(f"edit_expense_form_{expense.id}"):
        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0,
            value=float(expense.amount),
            key=f"expense_amount_{expense.id}",
        )
        category_name = st.selectbox("Category", category_names, index=current_index, key=f"expense_category_{expense.id}")
        expense_date = st.date_input("Expense date", value=expense.expense_date, key=f"expense_date_{expense.id}")
        payment_method = st.text_input("Payment method", value=expense.payment_method or "", key=f"expense_payment_{expense.id}")
        description = st.text_area("Description", value=expense.description or "", key=f"expense_description_{expense.id}")
        is_recurring = st.checkbox("Recurring expense", value=expense.is_recurring, key=f"expense_recurring_{expense.id}")
        col_save, col_cancel = st.columns(2)
        with col_save:
            save = st.form_submit_button("Save changes")
        with col_cancel:
            cancel = st.form_submit_button("Cancel")

    if cancel:
        st.rerun()

    if save:
        try:
            expense_service.update_expense(
                expense.id,
                ExpenseCreateSchema(
                    amount=amount,
                    category_id=category_options.get(category_name),
                    expense_date=expense_date,
                    payment_method=payment_method or None,
                    description=description or None,
                    is_recurring=is_recurring,
                ),
            )
            st.success("Expense updated successfully.")
            st.rerun()
        except BudgetFlowException as exc:
            st.error(str(exc))
