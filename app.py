import streamlit as st

from src.core.database import init_database
from src.seed.seed_data import seed_default_categories
from src.ui.pages.dashboard_page import render_dashboard_page
from src.ui.pages.expenses_page import render_expenses_page
from src.ui.pages.incomes_page import render_incomes_page
from src.ui.sidebar import render_sidebar


def main() -> None:
    st.set_page_config(page_title="BudgetFlow", layout="wide")
    init_database()
    seed_default_categories()

    page = render_sidebar()

    if page == "Dashboard":
        render_dashboard_page()
    elif page == "Incomes":
        render_incomes_page()
    elif page == "Expenses":
        render_expenses_page()


if __name__ == "__main__":
    main()
