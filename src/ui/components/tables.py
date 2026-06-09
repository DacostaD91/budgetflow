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
