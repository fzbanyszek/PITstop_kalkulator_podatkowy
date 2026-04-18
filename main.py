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

st.markdown("""
<style>
.language-box {
    position: fixed;
    bottom: 20px;
    width: 220px;
    z-index: 999;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("assets/logo_and_name.png", width=280)
    st.markdown("---")

    st.page_link("pages/home.py", label="Strona tytułowa")
    st.page_link("pages/kalkulator.py", label="Kalkulator podatkowy")
    st.page_link("pages/ustawienia.py", label="Ustawienia")

    st.markdown('<div class="language-box">', unsafe_allow_html=True)
    language = st.selectbox(
        "Język",
        ["Polski", "English"],
        index=0
    )
    st.markdown("</div>", unsafe_allow_html=True)

pg.run()