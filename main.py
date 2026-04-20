import streamlit as st

from translations import LANGUAGE_OPTIONS, translate, sync_language
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

home_page = st.Page("pages/home.py", title=t("page_home"),default=True)
calculator_page = st.Page("pages/calculator.py", title=t("page_calculator"))
results_page = st.Page("pages/results.py", title=t("page_results"))
settings_page = st.Page("pages/settings.py", title=t("page_settings"))

has_results = st.session_state.get("portfolio") is not None
pages = [home_page, calculator_page]

if has_results:
    pages.append(results_page)

pages.append(settings_page)

pg = st.navigation(
    pages,
    position="hidden",
)

if st.session_state.get("open_results_after_processing") and has_results:
    st.session_state.open_results_after_processing = False
    st.switch_page("pages/results.py")

current_label = next(
    label for label, code in LANGUAGE_OPTIONS.items()
    if code == st.session_state.language
)

with st.sidebar:
    st.image("assets/logo_and_name.png", width=280)
    st.markdown("---")

    st.page_link("pages/home.py", label=t("page_home"))
    st.page_link("pages/calculator.py", label=t("page_calculator"))
    if has_results:
        st.page_link("pages/results.py", label=t("page_results"))
    st.page_link("pages/settings.py", label=t("page_settings"))

    st.markdown("---")

    st.selectbox(
        t("language_label"),
        options=list(LANGUAGE_OPTIONS.keys()),
        key="language_selector",
        index=list(LANGUAGE_OPTIONS.keys()).index(current_label),
        on_change=sync_language,
    )

pg.run()
