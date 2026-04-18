import streamlit as st

from translations import LANGUAGE_OPTIONS, translate
from translations.common import TRANSLATIONS as COMMON_TRANSLATIONS

st.set_page_config(
    page_title="PITstop",
    page_icon="assets/logo_small.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "language" not in st.session_state:
    st.session_state.language = "en"

t = lambda key, **kwargs: translate(COMMON_TRANSLATIONS, key, **kwargs)

home_page = st.Page("pages/home.py", title=t("page_home"), icon="🏠", default=True)
calculator_page = st.Page("pages/kalkulator.py", title=t("page_calculator"), icon="📈")
settings_page = st.Page("pages/ustawienia.py", title=t("page_settings"), icon="⚙️")

pg = st.navigation(
    [home_page, calculator_page, settings_page],
    position="hidden",
)

with st.sidebar:
    st.image("assets/logo_and_name.png", width=280)
    st.markdown("---")

    st.page_link("pages/home.py", label=t("page_home"), icon="🏠")
    st.page_link("pages/kalkulator.py", label=t("page_calculator"), icon="📈")
    st.page_link("pages/ustawienia.py", label=t("page_settings"), icon="⚙️")

    st.markdown("---")

    selected_label = st.selectbox(
        t("language_label"),
        options=list(LANGUAGE_OPTIONS.keys()),
        index=list(LANGUAGE_OPTIONS.values()).index(st.session_state.language),
    )

    st.session_state.language = LANGUAGE_OPTIONS[selected_label]

pg.run()