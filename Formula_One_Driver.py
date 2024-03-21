from urllib.request import urlopen
import json
import pandas as pd


response = urlopen("https://api.openf1.org/v1/drivers")
# print(response.status_code) works 
data = json.loads(response.read().decode('utf-8'))
df = pd.DataFrame(data)

# filter columns 
driver_set = df[["full_name", "country_code","team_name","driver_number"]]

# Drop any potential duplicates
filtered_driver_set = driver_set.drop_duplicates(subset=["full_name", "country_code","team_name","driver_number"], keep='last')
filtered_driver_set.dropna(subset=['country_code'], inplace=True)



# CSV file creation
# filtered_driver_set.to_csv('filtered_driver_set_FINAL.csv', index=False)

