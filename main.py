from ibkr_classes.ibkrPortfolio import IbkrPortfolio

import time
import streamlit as st

st.set_page_config(page_title="Upload plików", page_icon="📁")

st.title("Upload wielu plików")
st.write("Wgraj kilka plików, a aplikacja pokaże postęp ich przetwarzania.")

uploaded_files = st.file_uploader(
    "Wybierz pliki",
    accept_multiple_files=True,
    type=None  # możesz tu wpisać np. ["pdf", "xlsx", "csv"]
)

if uploaded_files:
    st.success(f"Liczba wybranych plików: {len(uploaded_files)}")
    portfolio = IbkrPortfolio(*uploaded_files)
    portfolio.build_portfolio()

    if st.button("Przetwórz pliki"):
        st.dataframe(portfolio.cleaned_and_merged_df, use_container_width=True)
        progress_bar = st.progress(0, text="Start przetwarzania...")
        status_placeholder = st.empty()

        total_files = len(uploaded_files)

        for i, uploaded_file in enumerate(uploaded_files, start=1):
            # Tutaj możesz dodać własną logikę:
            # np. odczyt pliku, zapis na dysk, analizę itp.
            file_bytes = uploaded_file.read()

            # Symulacja pracy
            time.sleep(0.5)

            percent = int(i / total_files * 100)
            progress_bar.progress(
                percent,
                text=f"Przetwarzanie pliku {i}/{total_files}: {uploaded_file.name}"
            )

            status_placeholder.write(
                f"Przetworzono: **{uploaded_file.name}** "
                f"({len(file_bytes)} bajtów)"
            )

        status_placeholder.success("Wszystkie pliki zostały przetworzone.")
else:
    st.info("Najpierw wybierz co najmniej jeden plik.")