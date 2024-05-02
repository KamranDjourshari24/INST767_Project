import requests
import pandas as pd
from google.cloud import storage
from datetime import datetime

def main(request):
  gdp_lst = []
  url = (f"https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH")
  response = requests.get(url)
  data = response.json()["values"]["NGDP_RPCH"]
  for country in data.items():
    for year in country[-1]:
      gdp_dict = {
          "Country_code": country[0],
          "GDP_Change_Rate": country[-1][year],
          "Year": year
      }
      gdp_lst.append(gdp_dict)

  df = pd.DataFrame(gdp_lst)


  storage_client = storage.Client()
  bucket = storage_client.bucket('gdp_bank')
  filename = f'gdp_data_{datetime.now()}.csv'
  blob = bucket.blob(filename)
  blob.upload_from_string(df.to_csv(index=False), content_type='text/csv')

