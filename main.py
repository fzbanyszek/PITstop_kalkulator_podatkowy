import streamlit as st

st.set_page_config(
    page_title="PITstop",
    page_icon="assets/logo_small.png",
    layout="wide"
)

home_page = st.Page("pages/home.py", title="Strona tytułowa")
calculator_page = st.Page("pages/kalkulator.py", title="Kalkulator podatkowy")
settings_page = st.Page("pages/ustawienia.py", title="Ustawienia")

pg = st.navigation(
    [home_page, calculator_page, settings_page],
    position="hidden"
)

language_options = {
    "Polski": "pl",
    "English": "en"
}

if "language" not in st.session_state:
    st.session_state.language = "pl"

with st.sidebar:
    st.image("assets/logo_and_name.png", width=280)
    st.markdown("---")

    st.page_link("pages/home.py", label="Strona tytułowa")
    st.page_link("pages/kalkulator.py", label="Kalkulator podatkowy")
    st.page_link("pages/ustawienia.py", label="Ustawienia")

    selected_label = st.selectbox(
        "Język",
        list(language_options.keys()),
        index=list(language_options.values()).index(st.session_state.language)
    )

    st.session_state.language = language_options[selected_label]

pg.run()