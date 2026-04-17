import streamlit as st

st.markdown("""
<style>
button[title="View fullscreen"] {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

st.image("assets/logo_and_name.png", width=220)

st.title("PITstop")
st.subheader("Kalkulator podatkowy dla danych z Interactive Brokers")

st.markdown("""
Ta aplikacja pozwala:
- wczytać pliki CSV,
- zbudować portfel transakcji,
- policzyć zrealizowane zyski dla wybranego roku podatkowego,
- przejrzeć historię transakcji.
""")

st.info("Wybierz stronę z menu po lewej stronie.")