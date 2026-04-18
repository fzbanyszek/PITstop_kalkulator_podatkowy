import streamlit as st

st.set_page_config(
    page_title="PITstop",
    page_icon="assets/logo_small.png",
    layout="wide"
)

st.logo("assets/logo_and_name.png", size="large")

home_page = st.Page("pages/home.py", title="Strona tytułowa")
calculator_page = st.Page("pages/kalkulator.py", title="Kalkulator podatkowy")
settings_page = st.Page("pages/ustawienia.py", title="Ustawienia")

pg = st.navigation(
    [home_page, calculator_page, settings_page],
    position="sidebar"
)

pg.run()