import streamlit as st
import pandas as pd
from ibkr_classes.ibkrCalculator import IbkrCalculator
from ibkr_classes.ibkrPortfolio import IbkrPortfolio

st.set_page_config(page_title="PITstop - Kalkulator", page_icon="📁")

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
            st.rerun()

        except Exception as e:
            st.error(f"Błąd: {e}")

if st.session_state.portfolio is not None:
    st.divider()
    st.header("Kalkulacja zysków")

    df = st.session_state.portfolio.cleaned_and_merged_df

    df['Date/Time'] = pd.to_datetime(df['Date/Time'])
    available_years = sorted(df['Date/Time'].dt.year.unique().tolist(), reverse=True)

    col1, _ = st.columns([1, 2])
    with col1:
        selected_year = st.selectbox("Wybierz rok podatkowy:", available_years)

    profits_dict = IbkrCalculator.calculate_proceeds_by_symbol(st.session_state.portfolio, selected_year)
    total_profit = IbkrCalculator.calculate_total_proceeds(st.session_state.portfolio, selected_year)

    st.metric(label=f"Całkowity zrealizowany zysk w {selected_year}", value=f"{total_profit:,.2f} PLN")

    st.subheader("Zysk zrealizowany na poszczególnych akcjach")

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
    st.info("Wgraj i przetwórz pliki, aby odblokować wybór roku i kalkulację zysków.")