# import streamlit as st
# import pandas as pd
# from ibkr_classes.ibkrCalculator import IbkrCalculator
# from ibkr_classes.ibkrPortfolio import IbkrPortfolio
#
# st.set_page_config(page_title="Upload plików", page_icon="📁")
#
# if "portfolio" not in st.session_state:
#     st.session_state.portfolio = None
#
# st.title("PITstop - kalkulator podatkowy")
#
# uploaded_files = st.file_uploader(
#     "Wybierz pliki",
#     accept_multiple_files=True,
#     type=["csv"]
# )
#
# if uploaded_files:
#     st.success(f"Liczba wybranych plików: {len(uploaded_files)}")
#
#     if st.button("Przetwórz pliki"):
#         progress_bar = st.progress(0, text="Start przetwarzania...")
#         status_placeholder = st.empty()
#
#         try:
#             status_placeholder.info("Tworzenie obiektu portfela...")
#             portfolio = IbkrPortfolio(*uploaded_files)
#
#             status_placeholder.info("Przetwarzanie danych...")
#             last_percent = 0
#
#             for progress in portfolio.build_portfolio():
#                 percent = int(progress * 100)
#
#                 # zabezpieczenie, żeby progress nie cofał się przez zaokrąglenia
#                 if percent < last_percent:
#                     percent = last_percent
#                 last_percent = percent
#
#                 progress_bar.progress(
#                     percent,
#                     text=f"Przetwarzanie danych... {percent}%"
#                 )
#
#             progress_bar.progress(100, text="Przetwarzanie zakończone")
#             status_placeholder.success("Wszystkie pliki zostały przetworzone.")
#
#             st.subheader("Dane po przetworzeniu")
#             st.dataframe(portfolio.cleaned_and_merged_df, use_container_width=True)
#
#         except Exception as e:
#             status_placeholder.empty()
#             st.error(f"Błąd podczas przetwarzania plików: {e}")
# else:
#     st.info("Najpierw wybierz co najmniej jeden plik.")
#
#
#
#
# # --- KROK 2: WYBÓR ROKU I WYNIKI (Pojawia się tylko po przetworzeniu) ---
# if st.session_state.portfolio is not None:
#     st.divider()
#     st.header("Analiza zysków")
#
#     # Pobieramy dostępne lata z przetworzonych danych
#     df = st.session_state.portfolio.cleaned_and_merged_df
#     # Zakładam, że kolumna z datą nazywa się 'date' i jest typu datetime
#     available_years = sorted(pd.to_datetime(df['date']).dt.year.unique().tolist(), reverse=True)
#
#     col_selection, _ = st.columns([1, 2])
#     with col_selection:
#         selected_year = st.selectbox("Wybierz rok podatkowy:", available_years)
#
#     # Obliczamy zyski dla wybranego roku
#     profits_dict = IbkrCalculator.calculate_proceeds_by_symbol(st.session_state.portfolio, selected_year)
#     total_profit = IbkrCalculator.calculate_total_proceeds(st.session_state.portfolio, selected_year)
#
#     # Wyświetlanie sumarycznego wyniku
#     st.metric(label=f"Całkowity zrealizowany zysk w {selected_year}", value=f"{total_profit:,.2f} PLN")
#
#     # Tabela z wynikami per symbol
#     st.subheader("Zysk zrealizowany per instrument")
#
#     # Konwersja słownika na DataFrame do wyświetlenia
#     results_df = pd.DataFrame(list(profits_dict.items()), columns=['Symbol', 'Zysk PLN'])
#
#     # Sortowanie od największego zysku
#     results_df = results_df.sort_values(by="Zysk PLN", ascending=False)
#
#     st.dataframe(
#         results_df,
#         use_container_width=True,
#         hide_index=True,
#         column_config={
#             "Zysk PLN": st.column_config.NumberColumn(format="%.2f PLN")
#         }
#     )
#
#     # Opcjonalnie: Podgląd surowych danych
#     with st.expander("Pokaż historię transakcji (wszystkie lata)"):
#         st.dataframe(df, use_container_width=True)
# else:
#     st.info("Wgraj i przetwórz pliki, aby odblokować wybór roku i kalkulację zysków.")


import streamlit as st
import pandas as pd
from ibkr_classes.ibkrCalculator import IbkrCalculator
from ibkr_classes.ibkrPortfolio import IbkrPortfolio

st.set_page_config(page_title="PITstop - Kalkulator", page_icon="📁", layout="wide")

# 1. Inicjalizacja stanu sesji (Kluczowe!)
if "portfolio" not in st.session_state:
    st.session_state.portfolio = None

st.title("PITstop - kalkulator podatkowy")

uploaded_files = st.file_uploader(
    "Wybierz pliki",
    accept_multiple_files=True,
    type=["csv"]
)

if uploaded_files:
    st.success(f"Liczba wybranych plików: {len(uploaded_files)}")

    # Jeśli użytkownik kliknie przycisk, przetwarzamy i ZAPISUJEMY do sesji
    if st.button("Przetwórz pliki"):
        progress_bar = st.progress(0, text="Start przetwarzania...")
        status_placeholder = st.empty()

        try:
            status_placeholder.info("Tworzenie obiektu portfela...")
            portfolio_obj = IbkrPortfolio(*uploaded_files)

            for progress in portfolio_obj.build_portfolio():
                percent = int(progress * 100)
                progress_bar.progress(percent, text=f"Przetwarzanie danych... {percent}%")

            # ZAPIS DO SESJI - to sprawi, że dane nie znikną
            st.session_state.portfolio = portfolio_obj

            progress_bar.progress(100, text="Przetwarzanie zakończone")
            status_placeholder.success("Pliki przetworzone pomyślnie!")
            # Wymuszamy odświeżenie, aby od razu pokazać sekcję zysków
            st.rerun()

        except Exception as e:
            st.error(f"Błąd: {e}")

# 2. SEKCJA OBLICZEŃ - Pojawi się tylko gdy portfolio jest w sesji
if st.session_state.portfolio is not None:
    st.divider()
    st.header("Kalkulacja zysków")

    # Pobieramy dane z obiektu zapisanego w sesji
    df = st.session_state.portfolio.cleaned_and_merged_df

    # Wykrywanie dostępnych lat z kolumny Date/Time (na Twoim screenie to "Date/Time")
    df['Date/Time'] = pd.to_datetime(df['Date/Time'])
    available_years = sorted(df['Date/Time'].dt.year.unique().tolist(), reverse=True)

    col1, _ = st.columns([1, 2])
    with col1:
        selected_year = st.selectbox("Wybierz rok podatkowy:", available_years)

    # Obliczenia przy użyciu Twoich metod statycznych
    profits_dict = IbkrCalculator.calculate_proceeds_by_symbol(st.session_state.portfolio, selected_year)
    total_profit = IbkrCalculator.calculate_total_proceeds(st.session_state.portfolio, selected_year)

    # Wyświetlanie wyników
    st.metric(label=f"Całkowity zrealizowany zysk w {selected_year}", value=f"{total_profit:,.2f} PLN")

    st.subheader("Zysk zrealizowany na poszczególnych akcjach")

    # Tworzymy tabelę wyników
    results_df = pd.DataFrame(list(profits_dict.items()), columns=['Symbol', 'Zysk (PLN)'])
    results_df = results_df.sort_values(by="Zysk (PLN)", ascending=False)

    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Zysk (PLN)": st.column_config.NumberColumn(format="%.2f PLN")
        }
    )

    with st.expander("Zobacz historię transakcji"):
        st.dataframe(df, use_container_width=True)
else:
    # To jest komunikat, który widziałaś na screenie
    st.info("Wgraj i przetwórz pliki, aby odblokować wybór roku i kalkulację zysków.")