import yfinance as yf
import os
import pandas as pd
import json
from datetime import datetime

json_file_path = 'json'
if not os.path.exists(json_file_path):
    os.makedirs(json_file_path)

with open(f'{json_file_path}/symbols.json', 'r', encoding = 'utf-8') as file:
    data = json.load(file)

# Historical Data around 20 years.
symbols = data['ticker']
start_date = "2005-01-01"
end_date = datetime.today().strftime("%Y-%m-%d")

if not os.path.exists("csv_files"):
    os.makedirs("csv_files")

for symbol in symbols:
    stock_data = yf.download(symbol, start = start_date, end = end_date, interval = "1d")

    file_path = f"csv_files/{symbol}.csv"
    stock_data.to_csv(file_path)

    df = pd.read_csv(file_path)
    df.rename(columns = {'Price' : 'Date'}, inplace = True)
    table = df.iloc[2 : ].reset_index(drop = True)
    table.to_csv(file_path, index = False)

print("Historical Data Collected!")