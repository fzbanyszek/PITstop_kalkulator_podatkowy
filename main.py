import streamlit as st
from ibkr_classes.ibkrPortfolio import IbkrPortfolio

st.set_page_config(page_title="Upload plików", page_icon="📁")

st.title("PITstop - kalkulator podatkowy")
st.write("test")

uploaded_files = st.file_uploader(
    "Wybierz pliki",
    accept_multiple_files=True,
    type=["csv"]
)

if uploaded_files:
    st.success(f"Liczba wybranych plików: {len(uploaded_files)}")

    if st.button("Przetwórz pliki"):
        progress_bar = st.progress(0, text="Start przetwarzania...")
        status_placeholder = st.empty()

        try:
            status_placeholder.info("Tworzenie obiektu portfela...")
            portfolio = IbkrPortfolio(*uploaded_files)

            status_placeholder.info("Przetwarzanie danych...")
            last_percent = 0

            for progress in portfolio.build_portfolio():
                percent = int(progress * 100)

                # zabezpieczenie, żeby progress nie cofał się przez zaokrąglenia
                if percent < last_percent:
                    percent = last_percent
                last_percent = percent

                progress_bar.progress(
                    percent,
                    text=f"Przetwarzanie danych... {percent}%"
                )

            progress_bar.progress(100, text="Przetwarzanie zakończone")
            status_placeholder.success("Wszystkie pliki zostały przetworzone.")

            st.subheader("Dane po przetworzeniu")
            st.dataframe(portfolio.cleaned_and_merged_df, use_container_width=True)

        except Exception as e:
            status_placeholder.empty()
            st.error(f"Błąd podczas przetwarzania plików: {e}")
else:
    st.info("Najpierw wybierz co najmniej jeden plik.")