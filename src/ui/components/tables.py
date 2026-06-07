import streamlit as st


def render_dataframe_table(data):
    if data.empty:
        st.info("No records found.")
        return

    st.dataframe(data, use_container_width=True)
