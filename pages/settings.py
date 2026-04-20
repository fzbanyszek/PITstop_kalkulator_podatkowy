import streamlit as st

from calendar_files.calendar import global_calendar
from translations import translate
from translations.settings import TRANSLATIONS as SETTINGS_TRANSLATIONS
from translations.common import TRANSLATIONS as COMMON_TRANSLATIONS

t = lambda key, **kwargs: translate(SETTINGS_TRANSLATIONS, key, **kwargs)
tc = lambda key: translate(COMMON_TRANSLATIONS, key)

if "calendar_feedback" not in st.session_state:
    st.session_state.calendar_feedback = None

st.title(t("title"))
st.divider()

st.subheader(t("display_section"))
on = st.toggle(t("dark_mode"), disabled=True)

st.divider()
st.subheader(t("calendar_section"))

calendar_table_col, calendar_info_col = st.columns([1.25, 1])

with calendar_table_col:
    st.dataframe(
        global_calendar.closed_days_df,
        use_container_width=True
    )

    uploaded_file = st.file_uploader(t("calendar_upload_label"), type=["csv"])

    upload_col, reset_col = st.columns(2)
    with upload_col:
        upload_clicked = st.button(
            t("calendar_upload_button"),
            use_container_width=True
        )
    with reset_col:
        reset_clicked = st.button(
            t("calendar_reset_button"),
            use_container_width=True
        )

    calendar_feedback = st.empty()
    feedback_message_key = st.session_state.calendar_feedback
    if feedback_message_key is not None:
        calendar_feedback.success(t(feedback_message_key))
        st.session_state.calendar_feedback = None

with calendar_info_col:
    st.markdown(f"#### {t('calendar_info_title')}")
    st.markdown(
        f"""
{t("calendar_info_what")}

{t("calendar_info_usage")}

{t("calendar_info_custom")}

{t("calendar_info_recalculate")}
"""
    )

if upload_clicked:
    if uploaded_file is None:
        calendar_feedback.warning(t("calendar_upload_missing"))
    else:
        global_calendar.set_calendar(uploaded_file)
        st.session_state.calendar_feedback = "calendar_upload_success"
        st.rerun()

if reset_clicked:
    global_calendar.reset_calendar()
    st.session_state.calendar_feedback = "calendar_reset_success"
    st.rerun()



st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #808495; font-size: 0.9em;'>
    {tc("footer_authors")}
    </div>
    """,
    unsafe_allow_html=True
)
