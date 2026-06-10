import streamlit as st


def render_dataframe_table(data):
    if data.empty:
        st.info("No records found.")
        return

    st.dataframe(data, use_container_width=True)


def render_budget_vs_actual_table(data):
    if not data:
        st.info("No budget data available for this month.")
        return

    header_cols = st.columns([1.8, 1.4, 1.4, 1.4, 1.0, 1.5, 1.6])
    headers = ["Category", "Planned Amount", "Actual Amount", "Difference", "Usage %", "Status", "Actions"]
    for col, header in zip(header_cols, headers):
        col.caption(header)

    for item in data:
        row_cols = st.columns([1.8, 1.4, 1.4, 1.4, 1.0, 1.5, 1.6])
        row_cols[0].write(item["category_name"])
        row_cols[1].write(f"DOP {item['planned_amount']:,.2f}")
        row_cols[2].write(f"DOP {item['actual_amount']:,.2f}")
        row_cols[3].write(f"DOP {item['difference']:,.2f}")
        row_cols[4].write(f"{item['usage_percentage']:.2f}%")
        row_cols[5].write(item["status"])
        yield item, row_cols[6]


def render_debts_table(debts):
    if not debts:
        st.info("No debts found.")
        return

    headers = ["Name", "Lender", "Original", "Balance", "Rate", "Monthly", "Day", "Status", "Progress"]
    header_cols = st.columns([1.5, 1.5, 1.2, 1.2, 0.8, 1.2, 0.6, 0.9, 1.0])
    for col, header in zip(header_cols, headers):
        col.caption(header)

    for debt in debts:
        progress = 0 if debt.original_amount <= 0 else ((debt.original_amount - debt.current_balance) / debt.original_amount) * 100
        row_cols = st.columns([1.5, 1.5, 1.2, 1.2, 0.8, 1.2, 0.6, 0.9, 1.0])
        row_cols[0].write(debt.name)
        row_cols[1].write(debt.lender)
        row_cols[2].write(f"DOP {debt.original_amount:,.2f}")
        row_cols[3].write(f"DOP {debt.current_balance:,.2f}")
        row_cols[4].write("" if debt.interest_rate is None else f"{debt.interest_rate:.2f}%")
        row_cols[5].write("" if debt.monthly_payment is None else f"DOP {debt.monthly_payment:,.2f}")
        row_cols[6].write(debt.payment_day or "")
        row_cols[7].write(debt.status)
        row_cols[8].write(f"{progress:.2f}%")


def render_debt_payments_table(payments):
    if not payments:
        st.info("No payments found.")
        return

    headers = ["Date", "Debt", "Amount", "Payment Type", "Description"]
    header_cols = st.columns([1.2, 1.8, 1.2, 1.4, 2.4])
    for col, header in zip(header_cols, headers):
        col.caption(header)

    for payment in payments:
        row_cols = st.columns([1.2, 1.8, 1.2, 1.4, 2.4])
        row_cols[0].write(payment.payment_date)
        row_cols[1].write(payment.debt.name if payment.debt else "")
        row_cols[2].write(f"DOP {payment.amount:,.2f}")
        row_cols[3].write(payment.payment_type)
        row_cols[4].write(payment.description or "")
