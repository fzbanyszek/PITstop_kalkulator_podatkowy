from datetime import datetime

import pandas as pd


class Calendar:
    closed_days_list: list[datetime]


    def __init__(self, path_to_calendar, *paths_to_calendars):
        self.closed_days_df = pd.read_csv(path_to_calendar)
        self.closed_days_list = pd.to_datetime(
            self.closed_days_df["date"]
        ).tolist()

    def set_calendar(self, uploaded_csv_calendar):
        if uploaded_csv_calendar is not None:
            custom_calendar = pd.read_csv(uploaded_csv_calendar)
            self.closed_days_df = custom_calendar
            self.closed_days_list = pd.to_datetime(
                custom_calendar["date"]
            ).tolist()

    def reset_calendar(self):
        self.closed_days_df = pd.read_csv("calendar_files/nyse_closed_days_2024_2025.csv")
        self.closed_days_list = pd.to_datetime(
            self.closed_days_df["date"]
        ).tolist()

global_calendar = Calendar("calendar_files/nyse_closed_days_2024_2025.csv")
