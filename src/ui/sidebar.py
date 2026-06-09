import streamlit as st

from src.core.settings import APP_NAME


def render_sidebar():
    st.sidebar.title(APP_NAME)
    return st.sidebar.radio("Navigation", ["Dashboard", "Incomes", "Expenses", "Budgets"])
