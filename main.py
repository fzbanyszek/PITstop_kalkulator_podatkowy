from ibkr_classes.ibkrPortfolio import IbkrPortfolio
import time
import streamlit as st

st.set_page_config(page_title="Upload plików", page_icon="📁")

st.title("Upload wielu plików")
st.write("Wgraj kilka plików, a aplikacja pokaże postęp ich przetwarzania.")

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

        total_files = len(uploaded_files)

        # Pasek postępu dla plików
        for i, uploaded_file in enumerate(uploaded_files, start=1):
            percent = int(((i - 1) / total_files) * 100)
            progress_bar.progress(
                percent,
                text=f"Przygotowanie pliku {i}/{total_files}: {uploaded_file.name}"
            )
            status_placeholder.write(f"Przygotowywanie: **{uploaded_file.name}**")
            time.sleep(0.2)

        try:
            # Ważne: tworzenie i przetwarzanie dopiero po kliknięciu
            portfolio = IbkrPortfolio(*uploaded_files)
            portfolio.build_portfolio()

            progress_bar.progress(100, text="Przetwarzanie zakończone")
            status_placeholder.success("Wszystkie pliki zostały przetworzone.")

            st.subheader("Dane po przetworzeniu")
            st.dataframe(portfolio.cleaned_and_merged_df, use_container_width=True)

        except Exception as e:
            st.error(f"Błąd podczas przetwarzania plików: {e}")
else:
    st.info("Najpierw wybierz co najmniej jeden plik.")