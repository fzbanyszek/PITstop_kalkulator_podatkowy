from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

from calendar_files.calendar import global_calendar
from ibkr_classes.ibkrDataOperations import get_cleaned_df, get_applicable_exchange_rate, \
    get_data_from_file, get_settlement_date
from ibkr_classes.ibkrPosition import IbkrPosition
from ibkr_classes.ibkrTrade import IbkrTrade


class IbkrPortfolio:
    positions: dict[str, IbkrPosition]
    dataframes: list[pd.DataFrame]
    cleaned_and_merged_df: pd.DataFrame
    calendar = global_calendar
    exchange_rate_workers = 10

    def __init__(self, first_file, *other_files):
        self.files = [first_file] + list(other_files)

    def clean_raw_data_from_files(self):
        self.dataframes = []
        for path in self.files:
            raw_df = get_data_from_file(path)
            cleaned_df = get_cleaned_df(raw_df)
            self.dataframes.append(cleaned_df)

    def merge_cleaned_data(self):
        self.cleaned_and_merged_df = pd.concat(self.dataframes, ignore_index=True)

    def fetch_all_exchange_rates_into_df(self):
        total = len(self.cleaned_and_merged_df)

        if total == 0:
            return

        def fetch_exchange_rate(index, row):
            date_of_transaction = row['Date/Time']

            if pd.isna(date_of_transaction):
                return index, pd.NaT, None

            currency = row['Currency']
            settlement_date = get_settlement_date(date_of_transaction, self.calendar.closed_days_list)
            rate = get_applicable_exchange_rate(currency, settlement_date)

            return index, settlement_date, rate

        with ThreadPoolExecutor(max_workers=self.exchange_rate_workers) as executor:
            futures = [
                executor.submit(fetch_exchange_rate, index, row)
                for index, row in self.cleaned_and_merged_df.iterrows()
            ]

            for completed, future in enumerate(as_completed(futures), start=1):
                index, settlement_date, rate = future.result()

                self.cleaned_and_merged_df.at[index, 'Settlement Date'] = settlement_date
                self.cleaned_and_merged_df.at[index, 'Rate'] = rate

                if rate:
                    self.cleaned_and_merged_df.at[index, 'Proceeds in PLN'] = (
                        rate * float(self.cleaned_and_merged_df.at[index, 'Proceeds'])
                    )
                    self.cleaned_and_merged_df.at[index, 'Comm in PLN'] = (
                        rate * float(self.cleaned_and_merged_df.at[index, 'Comm/Fee'])
                    )

                yield completed / total

    def save_merged_and_cleaned_data_to_csv(self):
        self.cleaned_and_merged_df.to_csv("merged_and_cleaned.csv", index=False, encoding='utf-8')

    def load_portfolio_as_csv(self, file_path: str):
        try:
            df = pd.read_csv(file_path)
            if 'Date/Time' in df.columns:
                df['Date/Time'] = pd.to_datetime(df['Date/Time'], errors='coerce')
            self.cleaned_and_merged_df = df
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku pod ścieżką: {file_path}")
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")

    def create_positions(self):
        positions_dict = {}

        for _, row in self.cleaned_and_merged_df.iterrows():
            symbol = row["Symbol"]

            trade = IbkrTrade(
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
                positions_dict[symbol] = IbkrPosition(symbol)

            positions_dict[symbol].add_trade(trade)

        for position in positions_dict.values():
            position.sort_trades()

        self.positions = positions_dict

    def build_portfolio(self):
        self.clean_raw_data_from_files()
        self.merge_cleaned_data()

        for progress in self.fetch_all_exchange_rates_into_df():
            yield progress

        self.create_positions()



