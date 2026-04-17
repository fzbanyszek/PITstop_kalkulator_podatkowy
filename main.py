import streamlit as st

st.set_page_config(
    page_title="PITstop",
    page_icon="🏁",
    layout="wide"
)

st.title("PITstop")
st.subheader("Kalkulator podatkowy dla danych z Interactive Brokers")

st.markdown("""
Ta aplikacja pozwala:
- wczytać pliki CSV z danymi transakcyjnymi,
- zbudować portfel,
- policzyć zrealizowane zyski dla wybranego roku podatkowego,
- przejrzeć historię transakcji.
""")

st.info("Wybierz stronę z menu po lewej stronie.")