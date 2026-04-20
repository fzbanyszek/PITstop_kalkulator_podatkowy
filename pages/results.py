from html import escape

import pandas as pd
import streamlit as st

from ibkr_classes.ibkrCalculator import IbkrCalculator
from translations import translate
from translations.common import TRANSLATIONS as COMMON_TRANSLATIONS
from translations.results import TRANSLATIONS as RESULTS_TRANSLATIONS


t = lambda key, **kwargs: translate(RESULTS_TRANSLATIONS, key, **kwargs)
tc = lambda key: translate(COMMON_TRANSLATIONS, key)

if "portfolio" not in st.session_state:
    st.session_state.portfolio = None

if "results_feedback" not in st.session_state:
    st.session_state.results_feedback = None

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

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                t("profit_col"): st.column_config.NumberColumn(format="%.2f PLN")
            }
        )

    with st.expander(t("history_expander")):
        display_df = df.copy()
        display_df.index = display_df.index + 1
        st.dataframe(display_df, use_container_width=True)

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #808495; font-size: 0.9em;'>
    {tc("footer_authors")}
    </div>
    """,
    unsafe_allow_html=True
)
