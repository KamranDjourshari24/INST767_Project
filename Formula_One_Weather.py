from urllib.request import urlopen
import json
import pandas as pd


response = urlopen("https://api.openf1.org/v1/weather")
# print(response.status_code) to check if it works
data = json.loads(response.read().decode('utf-8'))
# convert to a data frame
df = pd.DataFrame(data)


# Include needed columns
weather_set = df[["air_temperature","humidity","meeting_key","pressure","rainfall","session_key","track_temperature","wind_direction","wind_speed"]]

#remove any possible duplicates
filtered_weather_set = weather_set.drop_duplicates(subset=["air_temperature","humidity","meeting_key","pressure","rainfall","session_key","track_temperature","wind_direction","wind_speed"], keep='first')


#create csv file
#filtered_weather_set.to_csv('filtered_weather_set_FINAL.csv', index=False)
