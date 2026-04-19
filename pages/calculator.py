import io
import zipfile
from pathlib import Path

import streamlit as st
import pandas as pd

from ibkr_classes.ibkrCalculator import IbkrCalculator
from ibkr_classes.ibkrPortfolio import IbkrPortfolio
from translations import translate
from translations.calculator import TRANSLATIONS as CALC_TRANSLATIONS
from translations.common import TRANSLATIONS as COMMON_TRANSLATIONS


t = lambda key, **kwargs: translate(CALC_TRANSLATIONS, key, **kwargs)
tc = lambda key: translate(COMMON_TRANSLATIONS, key)

if "portfolio" not in st.session_state:
    st.session_state.portfolio = None

st.title(t("title"))
st.divider()

with st.expander(t("tutorial_expander")):
    st.markdown(t("tutorial_content"))

    test1_path = Path("test_files/test_file_2024.csv")
    test2_path = Path("test_files/test_file_2025.csv")

    if test1_path.exists() and test2_path.exists():
        st.markdown(t("test_files_section"))

        with open(test1_path, "rb") as f:
            test1_bytes = f.read()

        with open(test2_path, "rb") as f:
            test2_bytes = f.read()

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("test_file_2024.csv", test1_bytes)
            zip_file.writestr("test_file_2025.csv", test2_bytes)
        zip_buffer.seek(0)

        st.download_button(
            label=t("download_test_zip"),
            data=zip_buffer,
            file_name="pitstop_test_files.zip",
            mime="application/zip",
            use_container_width=True
        )
    else:
        st.info(t("test_files_missing"))

st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    t("upload_label"),
    accept_multiple_files=True,
    type=["csv"]
)

if uploaded_files:
    st.success(t("files_selected", count=len(uploaded_files)))

    if st.button(t("process_button")):
        progress_bar = st.progress(0, text=t("progress_start"))
        status_placeholder = st.empty()

        try:
            status_placeholder.info(t("status_creating_portfolio"))
            portfolio_obj = IbkrPortfolio(*uploaded_files)

            for progress in portfolio_obj.build_portfolio():
                percent = int(progress * 100)
                progress_bar.progress(percent, text=t("progress_processing", percent=percent))

            st.session_state.portfolio = portfolio_obj

            progress_bar.progress(100, text=t("progress_done"))
            status_placeholder.success(t("success"))
            st.rerun()

        except Exception as e:
            st.error(t("error", error=e))

if st.session_state.portfolio is not None:
    st.divider()
    st.header(t("section_header"))

    df = st.session_state.portfolio.cleaned_and_merged_df.copy()
    df["Date/Time"] = pd.to_datetime(df["Date/Time"])
    available_years = sorted(df["Date/Time"].dt.year.unique().tolist(), reverse=True)

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

    st.metric(
        label=t("total_profit", year=selected_year),
        value=f"{total_profit:,.2f} PLN"
    )

    st.subheader(t("by_symbol_header"))

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
else:
    st.info(t("info_before_upload"))

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #808495; font-size: 0.9em;'>
    {tc("footer_authors")}
    </div>
    """,
    unsafe_allow_html=True
)