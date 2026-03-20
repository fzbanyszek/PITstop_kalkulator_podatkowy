import numpy as np
import pandas as pd


def get_prepared_ibkr_dataframe_for_calculations(df):
    selected_cols = ['Asset Category', 'Currency', 'Symbol', 'Date/Time', 'Quantity', 'Proceeds', 'Comm/Fee']
    df = df[selected_cols].iloc[0:]
    df['Rate'] = np.nan
    df['Proceeds in PLN'] = np.nan
    df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d, %H:%M:%S", errors="coerce")
    return df