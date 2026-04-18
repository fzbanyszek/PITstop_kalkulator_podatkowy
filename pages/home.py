import streamlit as st

from translations import translate
from translations.home import TRANSLATIONS as HOME_TRANSLATIONS

t = lambda key, **kwargs: translate(HOME_TRANSLATIONS, key, **kwargs)

st.image("assets/logo_and_name.png", width=700)

st.title(t("title"))
st.subheader(t("subtitle"))
st.markdown(t("description"))
st.info(t("info"))