import streamlit as st

LANGUAGE_OPTIONS = {
    "English": "en",
    "Polski": "pl",
}


def get_language() -> str:
    return st.session_state.get("language", "en")


def translate(translations: dict, key: str, **kwargs) -> str:
    lang = get_language()
    lang_dict = translations.get(lang, translations["en"])
    text = lang_dict.get(key, key)

    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text

    return text


def sync_language():
    selected_label = st.session_state.language_selector
    st.session_state.language = LANGUAGE_OPTIONS[selected_label]