from urllib.request import urlopen
import json
import pandas as pd


response = urlopen("https://api.openf1.org/v1/meetings")
# print(response.status_code) to verify if it works 
data = json.loads(response.read().decode('utf-8'))
df = pd.DataFrame(data)


# only include needed columns
meeting_set = df[["location", "meeting_name","year",]]


# Drop duplicates 
filtered_meeting_set = meeting_set.drop_duplicates(subset=["location", "meeting_name","year"], keep='last')


#CSV file creation
#filtered_meeting_set.to_csv('filtered_meeting_set_FINAL.csv', index=False)

