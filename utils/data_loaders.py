import pandas as pd
import io
import requests



def get_ibkr_data_from_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        filtr = "".join([line for line in f if line.startswith("Trades")])
        result = pd.read_csv(io.StringIO(filtr))
        return result


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




def set_exchange_rate_into_ibkr_dataframe(currency, date, df):

    return df