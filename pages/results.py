from html import escape

import pandas as pd
import streamlit as st

from ibkr_classes.ibkrCalculator import IbkrCalculator
from ibkr_classes.ibkrDataOperations import get_settlement_date
from ibkr_classes.pdf_report import generate_trade_history_pdf
from translations import translate
from translations.common import TRANSLATIONS as COMMON_TRANSLATIONS
from translations.results import TRANSLATIONS as RESULTS_TRANSLATIONS


t = lambda key, **kwargs: translate(RESULTS_TRANSLATIONS, key, **kwargs)
tc = lambda key: translate(COMMON_TRANSLATIONS, key)

if "portfolio" not in st.session_state:
    st.session_state.portfolio = None

if "results_feedback" not in st.session_state:
    st.session_state.results_feedback = None


def prepare_history_df(source_df: pd.DataFrame, portfolio) -> pd.DataFrame:
    history_df = source_df.copy()

    if "Settlement Date" not in history_df.columns:
        closed_days_list = portfolio.calendar.closed_days_list
        history_df["Settlement Date"] = history_df["Date/Time"].apply(
            lambda date: get_settlement_date(date, closed_days_list)
            if pd.notna(date)
            else pd.NaT
        )

    return history_df


st.markdown(
    """
    <style>
    .pitstop-total-card {
        border-radius: 1rem;
        margin-bottom: 1.25rem;
        padding: 1.15rem 1.25rem;
        border: 1px solid rgba(128, 132, 149, 0.24);
    }

    .pitstop-total-card.positive {
        background: rgba(42, 157, 143, 0.12);
        border-color: rgba(42, 157, 143, 0.42);
    }

    .pitstop-total-card.negative {
        background: rgba(209, 73, 91, 0.12);
        border-color: rgba(209, 73, 91, 0.42);
    }

    .pitstop-total-card.neutral {
        background: rgba(128, 132, 149, 0.08);
    }

    .pitstop-total-label {
        color: #808495;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }

    .pitstop-total-value {
        font-size: 2.4rem;
        font-weight: 800;
        line-height: 1.1;
    }

    .pitstop-total-value.positive {
        color: #2a9d8f;
    }

    .pitstop-total-value.negative {
        color: #d1495b;
    }

    .pitstop-total-value.neutral {
        color: inherit;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(t("title"))
st.divider()

if st.session_state.results_feedback == "success":
    st.success(t("success"))
    st.session_state.results_feedback = None

if st.session_state.portfolio is None:
    st.info(f"**{t('empty_title')}**\n\n{t('empty_message')}")
    st.page_link("pages/calculator.py", label=t("go_to_calculator"))
else:
    df = st.session_state.portfolio.cleaned_and_merged_df.copy()
    df["Date/Time"] = pd.to_datetime(df["Date/Time"])
    history_df = prepare_history_df(df, st.session_state.portfolio)
    available_years = sorted(df["Date/Time"].dt.year.unique().tolist(), reverse=True)

    total_profit_placeholder = st.empty()

    col1, _ = st.columns([1, 2])
    with col1:
        selected_year = st.selectbox(t("year_select"), available_years)

    profits_dict = IbkrCalculator.calculate_proceeds_by_symbol(
        st.session_state.portfolio,
        selected_year
    )
    total_profit = IbkrCalculator.calculate_total_proceeds(
        st.session_state.portfolio,
        selected_year
    )

    total_profit_state = "positive"
    if total_profit < 0:
        total_profit_state = "negative"
    elif total_profit == 0:
        total_profit_state = "neutral"

    total_profit_placeholder.markdown(
        f"""
        <div class="pitstop-total-card {total_profit_state}">
            <div class="pitstop-total-label">{escape(t("total_profit", year=selected_year))}</div>
            <div class="pitstop-total-value {total_profit_state}">{total_profit:,.2f} PLN</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander(t("by_symbol_header")):
        results_df = pd.DataFrame(
            list(profits_dict.items()),
            columns=[t("symbol_col"), t("profit_col")]
        ).sort_values(by=t("profit_col"), ascending=False)

        st.markdown(f"#### {t('profit_chart_title')}")
        st.bar_chart(
            results_df.set_index(t("symbol_col"))[[t("profit_col")]]
        )

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                t("profit_col"): st.column_config.NumberColumn(format="%.2f PLN")
            }
        )

    with st.expander(t("history_expander")):
        display_df = history_df.copy()
        settlement_dates = display_df.pop("Settlement Date")
        date_time_index = display_df.columns.get_loc("Date/Time") + 1
        display_df.insert(
            date_time_index,
            t("settlement_date_col"),
            settlement_dates
        )

        display_df.index = display_df.index + 1
        st.dataframe(display_df, use_container_width=True)

    report_df = history_df[history_df["Date/Time"].dt.year == selected_year].copy()
    report_pdf = generate_trade_history_pdf(
        report_df,
        selected_year,
        total_profit,
        t("pdf_report_title"),
        t("pdf_report_table_title"),
        t("pdf_total_profit_label"),
    )

    st.download_button(
        label=t("download_pdf_button"),
        data=report_pdf,
        file_name=f"pitstop_report_{selected_year}.pdf",
        mime="application/pdf",
        width="stretch",
    )

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #808495; font-size: 0.9em;'>
    {tc("footer_authors")}
    </div>
    """,
    unsafe_allow_html=True
)
