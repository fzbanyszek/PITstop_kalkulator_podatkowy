import io
import numpy as np
import pandas as pd
import requests

import pandas as pd
import numpy as np


def get_cleaned_df(df):
    selected_cols = ['Asset Category', 'Currency', 'Symbol', 'Date/Time', 'Quantity', 'Proceeds', 'Comm/Fee']

    # 1. Filtrowanie kategorii
    df = df[df['Asset Category'] != 'Forex'].copy()

    # 2. Czyszczenie separatorów w kolumnach liczbowych
    # Wybieramy kolumny, które powinny być liczbami
    numeric_cols = ['Quantity', 'Proceeds', 'Comm/Fee']

    for col in numeric_cols:
        if df[col].dtype == 'object':  # Jeśli kolumna jest tekstem
            # Usuwamy przecinki i zamieniamy na float
            df[col] = df[col].str.replace(',', '', regex=True).astype(float)

    # 3. Wybór kolumn i dalsza obróbka
    df = df[selected_cols]
    df['Rate'] = np.nan
    df['Proceeds in PLN'] = np.nan
    df['Comm in PLN'] = np.nan

    # Konwersja daty
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
    content = file.read()

    if isinstance(content, bytes):
        content = content.decode("utf-8-sig", errors="replace")

    filtr = "".join(
        line for line in content.splitlines(True)
        if line.startswith("Trades")
    )

    if not filtr.strip():
        raise ValueError(f"W pliku {getattr(file, 'name', 'bez nazwy')} nie znaleziono sekcji Trades.")

    return pd.read_csv(io.StringIO(filtr))

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
            return "No calendar_files for this date"
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
        elif result == "No calendar_files for this date":
            current_search_date -= pd.Timedelta(days=1)
        else:
            return f"Error: {result}"

def get_settlement_date(transaction_date, closed_days_list):
    transaction_date = pd.to_datetime(transaction_date).normalize()
    settlement_date = transaction_date + pd.Timedelta(days=1)
    while (settlement_date in closed_days_list) or (settlement_date.weekday() >= 5):
        settlement_date += pd.Timedelta(days=1)
    return settlement_date