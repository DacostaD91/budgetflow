import streamlit as st


def render_metric_card(label: str, value: str):
    st.metric(label=label, value=value)
