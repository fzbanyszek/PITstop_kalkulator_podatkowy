from utils.data_loaders import get_ibkr_data_from_csv, get_exchange_rate
from utils.data_operations import get_prepared_ibkr_dataframe_for_calculations

df_filtered_trades = get_ibkr_data_from_csv("data/ibkr_data.csv")
df_filtered_trades = get_prepared_ibkr_dataframe_for_calculations(df_filtered_trades)

df_filtered_trades.to_csv("data/filtered_result.csv", index=False, encoding='utf-8')


print(get_exchange_rate('USD', '2025-03-03'))


for index, row in df_filtered_trades.iterrows():
    wartosc = row['Date/Time']
    df_filtered_trades.at[index, 'Rate'] = 3.69

