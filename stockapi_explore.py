import requests
import pandas as pd

symbol = "FWONK"
month = "2024-03"
interval = "30"
url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol'
       f'={symbol}&interval={interval}min&month={month}&outputsize=full&'
       f'apikey=VYT21S4Y45H54ELK')
r = requests.get(url)
data = r.json()[f"Time Series ({interval}min)"]
df = pd.DataFrame.from_dict(data, orient='index')

print(df)
df.to_csv("StockApi.csv", header=True,index=True)

