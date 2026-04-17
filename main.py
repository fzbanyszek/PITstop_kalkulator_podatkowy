import streamlit as st

st.set_page_config(
    page_title="PITstopㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ",
    page_icon="🏁",
    layout="wide"
)

home_page = st.Page("views/home.py", title="Strona tytułowa", icon="🏠")
calculator_page = st.Page("views/kalkulator.py", title="Kalkulator podatkowy", icon="📈")
settings_page = st.Page("views/ustawienia.py", title="Ustawienia", icon="⚙️")

pg = st.navigation(
    [home_page, calculator_page, settings_page],
    position="sidebar"
)

st.set_page_config(
    page_title="PITstop",
    page_icon="assets/logo_and_name.png",
    layout="wide"
)

pg.run()