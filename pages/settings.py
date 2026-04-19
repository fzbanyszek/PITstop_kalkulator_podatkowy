import streamlit as st

from translations import translate
from translations.settings import TRANSLATIONS as SETTINGS_TRANSLATIONS
from translations.common import TRANSLATIONS as COMMON_TRANSLATIONS

t = lambda key, **kwargs: translate(SETTINGS_TRANSLATIONS, key, **kwargs)
tc = lambda key: translate(COMMON_TRANSLATIONS, key)

st.title(t("title"))
st.info(t("empty"))



st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #808495; font-size: 0.9em;'>
    {tc("footer_authors")}
    </div>
    """,
    unsafe_allow_html=True
)