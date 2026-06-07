import streamlit as st

from src.core.exceptions import BudgetFlowException
from src.core.service_factory import get_category_service, get_income_service
from src.schemas.income_schema import IncomeCreateSchema


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
    if not incomes:
        st.info("No records found.")
        return

    st.subheader("Income Records")
    header_cols = st.columns([0.8, 1.3, 1.6, 1.5, 1.2, 1.1, 2.0, 0.8])
    headers = ["ID", "Date", "Source", "Category", "Amount", "Recurring", "Description", ""]
    for col, header in zip(header_cols, headers):
        col.caption(header)

    for income in incomes:
        row_cols = st.columns([0.8, 1.3, 1.6, 1.5, 1.2, 1.1, 2.0, 0.8])
        row_cols[0].write(income.id)
        row_cols[1].write(income.income_date)
        row_cols[2].write(income.source)
        row_cols[3].write(income.category.name if income.category else "")
        row_cols[4].write(f"{income.amount:,.2f}")
        row_cols[5].write("Yes" if income.is_recurring else "No")
        row_cols[6].write(income.description or "")
        if row_cols[7].button("Edit", key=f"open_income_modal_{income.id}"):
            _render_income_edit_dialog(income, income_service, category_options)


@st.dialog("Edit Income")
def _render_income_edit_dialog(income, income_service, category_options: dict[str, int]) -> None:
    category_names = [""] + list(category_options.keys())
    current_category = income.category.name if income.category else ""
    current_index = category_names.index(current_category) if current_category in category_names else 0

    with st.form(f"edit_income_form_{income.id}"):
        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=100.0,
            value=float(income.amount),
            key=f"income_amount_{income.id}",
        )
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
            st.success("Income updated successfully.")
            st.rerun()
        except BudgetFlowException as exc:
            st.error(str(exc))
