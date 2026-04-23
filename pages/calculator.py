import io
import zipfile
from pathlib import Path

import streamlit as st

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

uploaded_files = st.file_uploader(
    t("upload_label"),
    accept_multiple_files=True,
    type=["csv"]
)

if uploaded_files:
    # st.success(t("files_selected", count=len(uploaded_files)))

    if st.button(t("process_button")):
        progress_bar = st.progress(0, text=t("progress_start"))
        status_placeholder = st.empty()

        try:
            portfolio_obj = IbkrPortfolio(*uploaded_files)

            for progress in portfolio_obj.build_portfolio():
                percent = int(progress * 100)
                progress_bar.progress(
                    percent,
                    text=t("progress_processing", percent=percent)
                )

            st.session_state.portfolio = portfolio_obj
            st.session_state.results_feedback = "success"
            st.session_state.open_results_after_processing = True

            progress_bar.progress(100, text=t("progress_done"))
            status_placeholder.success(t("success"))
            st.rerun()

        except Exception as e:
            st.error(t("error", error=e))

st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)

st.markdown(t("tutorial_content"))

test1_path = Path("test_files/test_file_2024.csv")
test2_path = Path("test_files/test_file_2025.csv")

if test1_path.exists() and test2_path.exists():
    st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
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
        width="content"
    )
else:
    st.info(t("test_files_missing"))

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #808495; font-size: 0.9em;'>
    {tc("footer_authors")}
    </div>
    """,
    unsafe_allow_html=True
)
