import io
import numpy as np
import pandas as pd
import requests

def get_cleaned_df(df):
    selected_cols = ['Asset Category', 'Currency', 'Symbol', 'Date/Time', 'Quantity', 'Proceeds', 'Comm/Fee']
    df = df[df['Asset Category'] != 'Forex'].copy()
    df = df[selected_cols].iloc[0:]
    df['Rate'] = np.nan
    df['Proceeds in PLN'] = np.nan
    df['Comm in PLN'] = np.nan
    df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d, %H:%M:%S", errors="coerce")
    df = df.dropna(subset=['Date/Time'])
    return df

def get_data_from_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        filtr = "".join([line for line in f if line.startswith("Trades")])
        result = pd.read_csv(io.StringIO(filtr))
        return result

def get_data_from_file(file):
    file.seek(0)
    return pd.read_csv(file)

def get_exchange_rate(currency, date):
    base_base = "https://api.nbp.pl/api/exchangerates/rates/A"
    url = f"{base_base}/{currency}/{date}/?format=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rate = data['rates'][0]['mid']
            return rate
        elif response.status_code == 404:
            return "No data for this date"
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def get_applicable_exchange_rate(currency, date):
    date_without_time = date.normalize()
    current_search_date = date_without_time - pd.Timedelta(days=1)

    while True:
        str_date = current_search_date.strftime("%Y-%m-%d")
        result = get_exchange_rate(currency, str_date)

        if isinstance(result, (float, int)):
            return result
        elif result == "No data for this date":
            current_search_date -= pd.Timedelta(days=1)
        else:
            return f"Error: {result}"