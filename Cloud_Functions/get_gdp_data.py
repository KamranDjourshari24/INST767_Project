import requests
import pandas as pd
from google.cloud import storage

def main(request):
  chng_dict = {}
  chnge_url = (f"https://www.imf.org/external/datamapper/api/v1/NGDP_RPCH")
  response_chnge = requests.get(chnge_url)
  chng_data = response_chnge.json()["values"]["NGDP_RPCH"]
  for country in chng_data.items():
    chng_dict[country[0]] = country[-1]


  country_codeurl = (f"https://www.imf.org/external/datamapper/api/v1/countries")
  response_country = requests.get(country_codeurl)
  countrydata = response_country.json()
  countries = list(countrydata["countries"].keys())

  gdp_lst = []

  for country in countries:
    try:
      gdp_url = (f"https://api.worldbank.org/v2/country/{country}/indicator/NY.GDP.MKTP.CD?format=json")
      gdp_response = requests.get(gdp_url)
      gdp_data = gdp_response.json()[1]
      for item in gdp_data:
        gdp_dict = {
            "Country_code": item["countryiso3code"],
            "Value": item['value'],
            "Year": item['date'],
            "GDP_Change_Rate": chng_dict[item["countryiso3code"]][item['date']]
        }
        gdp_lst.append(gdp_dict)
    except Exception as e:
        continue

  df = pd.DataFrame(gdp_lst)


  storage_client = storage.Client()
  bucket = storage_client.bucket('gdp_bank')
  filename = 'gdp_data.csv'
  blob = bucket.blob(filename)
  blob.upload_from_string(df.to_csv(index=False), content_type='text/csv')

  return f"File {filename} uploaded to {bucket.name}."