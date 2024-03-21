import requests
import pandas as pd


url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol'
       '=MSFT&interval=30min&apikey=VYT21S4Y45H54ELK')
r = requests.get(url)
data = r.json()["Time Series (30min)"]
df = pd.DataFrame.from_dict(data, orient='index')

df.to_csv("StockApi.csv", header=True,index=True)

