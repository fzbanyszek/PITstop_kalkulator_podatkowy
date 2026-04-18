import streamlit as st

from translations import translate
from translations.ustawienia import TRANSLATIONS as SETTINGS_TRANSLATIONS

t = lambda key, **kwargs: translate(SETTINGS_TRANSLATIONS, key, **kwargs)

st.title(t("title"))
st.info(t("empty"))