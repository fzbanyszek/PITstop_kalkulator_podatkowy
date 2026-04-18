import streamlit as st
from translations import translate
from translations.home import TRANSLATIONS as HOME_TRANSLATIONS

th = lambda key: translate(HOME_TRANSLATIONS, key)

st.title(th("title"))
st.write(th("intro"))

st.divider()

st.header(th("how_it_works_title"))
st.write(th("how_it_works_desc"))


col1, col2 = st.columns(2)

with col1:
    st.subheader(th("fifo_title"))
    st.write(th("fifo_desc"))

    st.subheader(th("nbp_title"))
    st.write(th("nbp_desc"))

with col2:
    st.subheader(th("settlement_title"))
    st.write(th("settlement_desc"))

    st.subheader(th("results_title"))
    st.write(th("results_desc"))

st.divider()

st.header(th("more_than_calc_title"))
st.write(th("more_than_calc_desc"))

st.info(f"**{th('review_title')}**: {th('review_desc')}")
st.info(f"**{th('grouping_title')}**: {th('grouping_desc')}")

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