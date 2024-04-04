import requests
import json
import pandas as pd

url = "https://api.travelpayouts.com/v2/prices/month-matrix"
querystring = {
    "currency": "usd",
    "show_to_affiliates": "true",
    "origin": "IAD",
    "destination": "MEL"
}
headers = {'x-access-token': '0d8ad327091b98ebf7730ab78be03a0c'}

response = requests.request("GET", url, headers=headers, params=querystring)
data = response.json()

# Convert to DataFrame
df = pd.DataFrame(data['data'])


# only include needed columns
flight_set = df[["depart_date","origin", "destination","value"]]

print(flight_set)

# FLIGHTS API (ATTEMPTING CALENDER OF PRICES FOR A MONTH)

#flight_set.to_csv('flight_set_sample.csv', index=False)