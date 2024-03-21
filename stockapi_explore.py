import requests
import pandas as pd


url = (f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symb'
       'ol=IBM&interval=5min&apikey=demo')
r = requests.get(url)
data = r.json()["Time Series (5min)"]
df = pd.DataFrame.from_dict(data, orient='index')

print(df)
