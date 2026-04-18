import streamlit as st

st.set_page_config(
    page_title="PITstop",
    page_icon="assets/logo_small.png",
    layout="wide"
)

with st.sidebar:
    st.html("""
        <div style="padding: 0.5rem 0 1rem 0;">
            <img src="app/static/logo_and_name.png"
                 style="width: 260px; max-width: 100%; height: auto; display: block;">
        </div>
    """)

home_page = st.Page("pages/home.py", title="Strona tytułowa")
calculator_page = st.Page("pages/kalkulator.py", title="Kalkulator podatkowy")
settings_page = st.Page("pages/ustawienia.py", title="Ustawienia")

pg = st.navigation(
    [home_page, calculator_page, settings_page],
    position="sidebar"
)

pg.run()