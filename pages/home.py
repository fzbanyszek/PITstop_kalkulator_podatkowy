from html import escape

import streamlit as st
from translations.home import TRANSLATIONS as HOME_TRANSLATIONS
from translations import translate
from translations.common import TRANSLATIONS as COMMON_TRANSLATIONS


th = lambda key: translate(HOME_TRANSLATIONS, key)
tc = lambda key: translate(COMMON_TRANSLATIONS, key)


def render_highlight_card(title: str, description: str):
    st.markdown(
        f"""
        <div class="pitstop-highlight-card">
            <div class="pitstop-highlight-title">{escape(title)}</div>
            <div class="pitstop-highlight-body">{escape(description)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
    .pitstop-lead {
        border-left: 4px solid #f4a261;
        background: rgba(244, 162, 97, 0.12);
        border-radius: 0.75rem;
        padding: 1rem 1.1rem;
        margin: 0.75rem 0 1.5rem;
        line-height: 1.6;
    }

    .pitstop-highlight-card {
        border: 1px solid rgba(128, 132, 149, 0.25);
        border-radius: 0.9rem;
        padding: 1rem 1.1rem;
        margin-bottom: 1rem;
        background: rgba(128, 132, 149, 0.08);
    }

    .pitstop-highlight-title {
        display: inline-block;
        margin-bottom: 0.55rem;
        padding: 0.2rem 0.55rem;
        border-radius: 999px;
        background: rgba(42, 157, 143, 0.14);
        color: #2a9d8f;
        font-weight: 700;
    }

    .pitstop-highlight-body {
        line-height: 1.55;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(th("title"))
st.markdown(
    f"""
    <div class="pitstop-lead">
        {escape(th("intro"))}
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.header(th("how_it_works_title"))
st.write(th("how_it_works_desc"))


col1, col2 = st.columns(2)

with col1:
    render_highlight_card(th("fifo_title"), th("fifo_desc"))

    render_highlight_card(th("nbp_title"), th("nbp_desc"))

    render_highlight_card(th("calendar_settings_title"), th("calendar_settings_desc"))

with col2:
    render_highlight_card(th("settlement_title"), th("settlement_desc"))

    render_highlight_card(th("results_title"), th("results_desc"))

st.divider()

st.header(th("more_than_calc_title"))
st.write(th("more_than_calc_desc"))

st.markdown(f"- **{th('review_title')}**: {th('review_desc')}")
st.markdown(f"- **{th('grouping_title')}**: {th('grouping_desc')}")


st.divider()

st.header(th("privacy_title"))
st.write(th("privacy_desc"))

st.markdown(f"- **{th('no_retention_title')}**: {th('no_retention_desc')}")
st.markdown(f"- **{th('transparency_title')}**: {th('transparency_desc')}")
st.markdown(f"- **{th('anon_title')}**: {th('anon_desc')}")

st.divider()

st.header(th("test_files_title"))
st.write(th("test_files_desc"))

st.warning(f"**{th('legal_title')}**: {th('legal_desc')}")


st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #808495; font-size: 0.9em;'>
    {tc("footer_authors")}
    </div>
    """,
    unsafe_allow_html=True
)
