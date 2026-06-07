import pandas as pd
import plotly.express as px
import streamlit as st


def render_expenses_by_category_chart(data):
    if not data:
        st.info("No expense data available for this month.")
        return

    dataframe = pd.DataFrame(data)
    figure = px.pie(dataframe, names="category", values="amount")
    st.plotly_chart(figure, use_container_width=True)
