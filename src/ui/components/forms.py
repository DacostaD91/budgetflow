import streamlit as st


def render_submit_button(label: str) -> bool:
    return st.form_submit_button(label)
