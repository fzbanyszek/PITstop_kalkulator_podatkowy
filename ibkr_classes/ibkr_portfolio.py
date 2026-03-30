import io
from collections import defaultdict

import numpy as np
import pandas as pd
import requests

from ibkr_classes.ibkr_position import Position
from ibkr_classes.ibkr_trade import Trade


class Portfolio:
    positions: dict[str, Position]

    def __init__(self, first_path, *other_paths):
        self.paths = [first_path] + list(other_paths)
        self.dataframes = []
        for path in self.paths:

            raw_df = Portfolio.get_data_from_csv(path)

            prepared_df = Portfolio.get_prepared_dataframe(raw_df)

            self.dataframes.append(prepared_df)

        self.ibkr_prepared_for_calc_df = pd.concat(self.dataframes, ignore_index=True)


    @staticmethod
    def get_data_from_csv(path):
        with open(path, 'r', encoding='utf-8') as f:
            filtr = "".join([line for line in f if line.startswith("Trades")])
            result = pd.read_csv(io.StringIO(filtr))
            return result


    @staticmethod
    def get_prepared_dataframe(df):
        selected_cols = ['Asset Category', 'Currency', 'Symbol', 'Date/Time', 'Quantity', 'Proceeds', 'Comm/Fee']

        df = df[df['Asset Category'] != 'Forex'].copy()

        df = df[selected_cols].iloc[0:]
        df['Rate'] = np.nan
        df['Proceeds in PLN'] = np.nan
        df['Comm in PLN'] = np.nan
        df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d, %H:%M:%S", errors="coerce")
        df = df.dropna(subset=['Date/Time'])
        return df

    @staticmethod
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

    @staticmethod
    def get_applicable_exchange_rate(currency, date):
        date_without_time = date.normalize()
        current_search_date = date_without_time - pd.Timedelta(days=1)

        while True:
            str_date = current_search_date.strftime("%Y-%m-%d")
            result = Portfolio.get_exchange_rate(currency, str_date)

            if isinstance(result, (float, int)):
                return result
            elif result == "No data for this date":
                current_search_date -= pd.Timedelta(days=1)
            else:
                return f"Error: {result}"

    @staticmethod
    def fetch_all_exchange_rates_into_ibkr_dataframe(df):
        for index, row in df.iterrows():
            date_of_transaction = row['Date/Time']
            if pd.notna(date_of_transaction):
                currency = row['Currency']
                rate = Portfolio.get_applicable_exchange_rate(currency, date_of_transaction)

                df.at[index, 'Rate'] = rate
                if rate:
                    df.at[index, 'Proceeds in PLN'] = rate * float(row['Proceeds'])
                    df.at[index, 'Comm in PLN'] = rate * float(row['Comm/Fee'])


    def save_all_data_to_csv(self):
        Portfolio.fetch_all_exchange_rates_into_ibkr_dataframe(self.ibkr_prepared_for_calc_df)

        self.ibkr_prepared_for_calc_df.to_csv("merged.csv", index=False, encoding='utf-8')




    def load_portfolio_csv(self, file_path: str):
        try:
            df = pd.read_csv(file_path)
            if 'Date/Time' in df.columns:
                df['Date/Time'] = pd.to_datetime(df['Date/Time'], errors='coerce')
            self.ibkr_prepared_for_calc_df = df
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku pod ścieżką: {file_path}")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")

    def createPositions(self):
        positions_dict = {}

        for _, row in self.ibkr_prepared_for_calc_df.iterrows():
            symbol = row["Symbol"]

            trade = Trade(
                asset=row["Asset Category"],
                currency=row["Currency"],
                symbol=row["Symbol"],
                date=row["Date/Time"],
                quantity=row["Quantity"],
                proceeds=row["Proceeds"],
                comm_fee=row["Comm/Fee"],
                rate=row["Rate"],
                proceeds_in_PLN=row["Proceeds in PLN"],
                comm_in_PLN=row["Comm in PLN"]
            )

            if symbol not in positions_dict:
                positions_dict[symbol] = Position(symbol)

            positions_dict[symbol].add_trade(trade)

        self.positions = positions_dict




        
