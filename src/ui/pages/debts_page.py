import streamlit as st

from src.core.exceptions import BudgetFlowException
from src.core.service_factory import get_debt_service
from src.schemas.debt_schema import DebtCreateSchema, DebtPaymentCreateSchema
from src.ui.components.charts import render_debt_balance_chart
from src.ui.components.metrics import render_debt_summary_metrics
from src.ui.components.tables import render_debt_payments_table, render_debts_table


def render_debts_page() -> None:
    st.title("Debts")
    debt_service = get_debt_service()

    summary = debt_service.get_debt_summary()
    render_debt_summary_metrics(summary)

    _render_create_debt_form(debt_service)
    _render_payment_form(debt_service)

    active_debts = debt_service.get_active_debts()
    paid_debts = debt_service.get_paid_debts()

    st.subheader("Debt Balance Chart")
    render_debt_balance_chart(_build_debt_chart_data(debt_service.get_all_debts()))

    tab_active, tab_paid, tab_payments = st.tabs(["Active Debts", "Paid Debts", "Payment History"])
    with tab_active:
        render_debts_table(active_debts)
    with tab_paid:
        render_debts_table(paid_debts)
    with tab_payments:
        _render_payment_history(debt_service)


def _render_create_debt_form(debt_service) -> None:
    st.subheader("Create Debt")
    with st.form("debt_form"):
        col_name, col_lender = st.columns(2)
        with col_name:
            name = st.text_input("Name")
        with col_lender:
            lender = st.text_input("Lender")

        col_original, col_balance = st.columns(2)
        with col_original:
            original_amount = st.number_input("Original amount", min_value=0.0, step=1000.0)
        with col_balance:
            current_balance = st.number_input("Current balance", min_value=0.0, step=1000.0)

        col_rate, col_monthly, col_day = st.columns(3)
        with col_rate:
            interest_rate = st.number_input("Interest rate", min_value=0.0, step=0.1)
        with col_monthly:
            monthly_payment = st.number_input("Monthly payment", min_value=0.0, step=500.0)
        with col_day:
            payment_day = st.number_input("Payment day", min_value=1, max_value=31, value=1, step=1)

        col_start, col_end = st.columns(2)
        with col_start:
            start_date = st.date_input("Start date", value=None)
        with col_end:
            end_date = st.date_input("End date", value=None)

        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add debt")

    if submitted:
        try:
            debt_service.create_debt(
                DebtCreateSchema(
                    name=name,
                    lender=lender,
                    original_amount=original_amount,
                    current_balance=current_balance,
                    interest_rate=interest_rate,
                    monthly_payment=monthly_payment,
                    payment_day=int(payment_day),
                    start_date=start_date,
                    end_date=end_date,
                    notes=notes or None,
                )
            )
            st.success("Debt created successfully.")
            st.rerun()
        except BudgetFlowException as exc:
            st.error(str(exc))


def _render_payment_form(debt_service) -> None:
    active_debts = debt_service.get_active_debts()
    if not active_debts:
        return

    st.subheader("Register Payment")
    debt_options = {f"{debt.name} - {debt.lender}": debt.id for debt in active_debts}
    with st.form("debt_payment_form"):
        debt_label = st.selectbox("Debt", list(debt_options.keys()))
        amount = st.number_input("Payment amount", min_value=0.0, step=500.0)
        payment_date = st.date_input("Payment date")
        payment_type = st.selectbox("Payment type", ["regular", "extra_principal"])
        description = st.text_area("Payment description")
        submitted = st.form_submit_button("Register payment")

    if submitted:
        try:
            debt_service.register_payment(
                DebtPaymentCreateSchema(
                    debt_id=debt_options[debt_label],
                    amount=amount,
                    payment_date=payment_date,
                    payment_type=payment_type,
                    description=description or None,
                )
            )
            st.success("Payment registered successfully.")
            st.rerun()
        except BudgetFlowException as exc:
            st.error(str(exc))


def _render_payment_history(debt_service) -> None:
    debts = debt_service.get_all_debts()
    debt_options = {"All debts": None} | {f"{debt.name} - {debt.lender}": debt.id for debt in debts}
    selected_debt = st.selectbox("Debt filter", list(debt_options.keys()))
    debt_id = debt_options[selected_debt]

    if debt_id is None:
        payments = []
        for debt in debts:
            payments.extend(debt_service.get_payments_by_debt(debt.id))
    else:
        payments = debt_service.get_payments_by_debt(debt_id)

    payments = sorted(payments, key=lambda payment: payment.payment_date, reverse=True)
    render_debt_payments_table(payments)


def _build_debt_chart_data(debts) -> list[dict]:
    return [
        {
            "name": debt.name,
            "current_balance": debt.current_balance,
            "status": debt.status,
        }
        for debt in debts
    ]
