import requests
import pandas as pd
from google.cloud import storage
import datetime

def main(request):
    race_list = []
    now = datetime.datetime.now()
    current_year = now.year
    years = range(2005, current_year+1)

    for year in years:
        url = f"http://ergast.com/api/f1/{year}.json"
        response = requests.get(url)
        data = response.json()
        races = data['MRData']['RaceTable']['Races']

        for race in races:
            location_name = race['Circuit']['Location']['locality']
            country_name = race['Circuit']['Location']['country']
        
            race_info = {
                'Race Name': race['raceName'],
                'Date': race['date'],
                'Time': race['time'],
                'Circuit': race['Circuit']['circuitName'],
                'Location': location_name,
                'Country': country_name,
                'Year': year
            }
            race_list.append(race_info)

    df = pd.DataFrame(race_list)

    storage_client = storage.Client()
    bucket = storage_client.bucket('f1_race_info')
    filename = f'F1_race.csv'
    blob = bucket.blob(filename)
    blob.upload_from_string(df.to_csv(index=False), content_type='text/csv')

    return f"File {filename} uploaded to {bucket.name}."

