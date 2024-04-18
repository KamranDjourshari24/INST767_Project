import requests
import pandas as pd

# Geo names function for Country Codes
def get_country_code(country_name):
    if country_name.lower() in ['usa', 'united states']:
        return 'USA'
    else:
        username = "saranram19" 
        url = f"http://api.geonames.org/searchJSON?q={country_name}&maxRows=1&username={username}"
        response = requests.get(url)
        data = response.json()
        if 'geonames' in data and data['geonames'] and 'countryCode' in data['geonames'][0]:
            country_code = data['geonames'][0]['countryCode']
            iso3_url = "http://country.io/iso3.json"
            iso3_response = requests.get(iso3_url)
            iso3_data = iso3_response.json()
            return iso3_data.get(country_code)
        else:
            return None

#GDP Function for country Codes and GDP vals
def get_gdp(country_code, year):
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.CD?format=json&date={year}"
    response = requests.get(url)
    data = response.json()
    if data[1]:
        gdp_data = next((item for item in data[1] if item['value'] is not None), None)
        if gdp_data:
            return gdp_data['value']
    return None

# Year ranges
years = range(2005, 2023)
race_list = []

#F1 API call
for year in years:
    url = f"http://ergast.com/api/f1/{year}.json"
    payload = {}
    headers = {}
    response = requests.get(url, headers=headers, data=payload)
    data = response.json()

    races = data['MRData']['RaceTable']['Races']

    for race in races:
        location_name = race['Circuit']['Location']['locality']
        country_name = race['Circuit']['Location']['country']
        country_code = get_country_code(country_name)
        # Will get the GDP based off of country code and the specific year
        gdp = get_gdp(country_code, year)
        race_info = {
            'Race Name': race['raceName'],
            'Date': race['date'],
            'Time': race['time'],
            'Circuit': race['Circuit']['circuitName'],
            'Location': location_name,
            'Country': country_name,
            'Country Code': country_code,
            'GDP': gdp,
            'Year': year
        }
        race_list.append(race_info)
# Put into dataframe
df = pd.DataFrame(race_list)
#df.to_csv('F1_GDP_Final.csv', index=False)
print(df)