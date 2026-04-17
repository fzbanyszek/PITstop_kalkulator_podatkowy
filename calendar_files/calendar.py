from datetime import datetime

import pandas as pd


class Calendar:
    closed_days_list: list[datetime]


    def __init__(self, path_to_calendar, *paths_to_calendars):
        self.closed_days_df = pd.read_csv(path_to_calendar)
        self.closed_days_list = pd.to_datetime(
            self.closed_days_df["date"]
        ).tolist()



