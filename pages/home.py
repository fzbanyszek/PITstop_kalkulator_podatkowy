import streamlit as st


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

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #808495; font-size: 0.9em;'>
    Developed by <b>Karolina Ratajczyk</b> and <b>Filip Zbanyszek</b>
    </div>
    """,
    unsafe_allow_html=True
)