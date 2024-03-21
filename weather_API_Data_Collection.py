import requests
import pandas as pd
import datetime

# API endpoint
url = "https://api.weatherbit.io/v2.0/history/daily"

# Access key
api_key = '83c0dfe4c6814fbf8259f28c2413c8cb'

# Location parameters
postal_code = '27601'
country_code = 'US'

# Taking 3 months historical data from Nov 2023 to Jan 2024
start_date_for_Daily = datetime.date(2023, 11, 1)
end_date_for_Daily = datetime.date(2024, 1, 31)

# Parameters for API request
params = {
    'postal_code': postal_code,
    'country': country_code,
    'start_date': start_date_for_Daily,
    'end_date': end_date_for_Daily,
    'key': api_key
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Define headers
headers = [
    '[Satellite based] average cloud coverage (%)',
    'Date (YYYY-MM-DD)',
    'Average dew point (default Celsius)',
    'Average diffuse horizontal solar irradiance (W/m^2) [Clear Sky]',
    'Average direct normal solar irradiance (W/m^2) [Clear Sky]',
    'Average global horizontal solar irradiance (W/m^2)',
    'Maximum value of diffuse horizontal solar irradiance in day (W/m^2) [Clear Sky]',
    'Maximum value of direct normal solar irradiance in day (W/m^2) [Clear Sky]',
    'Maximum value of global horizontal solar irradiance in day (W/m^2) [Clear Sky]',
    'Maximum temperature (default Celsius)',
    'Time of daily maximum temperature UTC (Unix Timestamp)',
    'Maximum UV Index (0-11+)',
    'Direction of maximum 2 minute wind gust (degrees)',
    'Maximum 2 minute wind speed (m/s)',
    'Time of maximum wind gust UTC (Unix Timestamp)',
    'Minimum temperature (default Celsius)',
    'Time of daily minimum temperature UTC (Unix Timestamp)',
    'Accumulated precipitation (default mm)',
    'Accumulated precipitation [satellite/radar estimated] (default mm)',
    'Average pressure (mb)',
    'Data revision status - interim (subject to revisions) or final',
    'Average relative humidity (%)',
    'Average sea level pressure (mb)',
    'Accumulated snowfall (default mm)',
    'Snow Depth (default mm)',
    'Average solar radiation (W/M^2)',
    'Day total diffuse horizontal solar irradiance (W/m^2) [Clear Sky]',
    'Day total direct normal solar irradiance (W/m^2) [Clear Sky]',
    'Day total global horizontal solar irradiance (W/m^2) [Clear Sky]',
    'Total solar radiation (W/M^2)',
    'Average temperature (default Celsius)',
    'Timestamp UTC (Unix Timestamp)',
    'Average wind direction (degrees)',
    'Wind gust speed (m/s)',
    'Average wind speed (Default m/s)'
]

# Print the response JSON
print(data)

weather_data = []

# Append the data to the list if 'data' key exists
if 'data' in data:
    weather_data.extend(data['data'])

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(weather_data)

# Set the headers
df.columns = headers

# Save the DataFrame to an Excel file
excel_file = 'Daily_Historical_weather_data.xlsx'
df.to_excel(excel_file, index=False)
print(f"Data has been saved to {excel_file}.")

# Accessing hourly api to fetch historical hourly whether data

city = "Raleigh,NC"
start_date_for_Hourly = "2024-03-01"
end_date_for_Hourly = "2024-03-20"

url = f"https://api.weatherbit.io/v2.0/history/hourly?city={city}&start_date={start_date_for_Hourly}&end_date={end_date_for_Hourly}&tz=local&key={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    # Extract relevant columns from the JSON
    columns = [
        "app_temp", "azimuth", "clouds", "datetime",
        "dewpt", "ghi", "dni", "elev_angle", "ghi_clear_sky",
        "h_angle", "pod", "precip", "pres", "revision",
        "rh", "slp", "snow", "solar_rad", "temp", "timestamp_local",
        "timestamp_utc", "ts", "uv", "vis", "weather",
        "wind_dir", "wind_gust_spd", "wind_spd"
    ]
    # Defining the new headers (which are descriptions of the json columns)
    new_columns = [
        "Apparent/Feels Like temperature (default Celsius)",
        "Solar azimuth angle (degrees)",
        "[Satellite based] cloud coverage (%)",
        "Date UTC (YYYY-MM-DD:HH) [Deprecated]",
        "Dew point (default Celsius)",
        "Diffuse horizontal solar irradiance (W/m^2) [Clear Sky]",
        "Direct normal solar irradiance (W/m^2) [Clear Sky]",
        "Solar elevation angle (degrees)",
        "Global horizontal solar irradiance (W/m^2) [Clear Sky]",
        "[DEPRECATED] Solar hour angle (degrees)",
        "Part of the day (d = day / n = night)",
        "Accumulated liquid equivalent precipitation (default mm)",
        "Pressure (mb)",
        "Data revision status - interim (subject to revisions) or final",
        "Relative humidity (%)",
        "Sea level pressure (mb)",
        "Accumulated snowfall (default mm)",
        "Estimated Solar Radiation (W/m^2)",
        "Temperature (default Celsius)",
        "Timestamp at Local time",
        "Timestamp at UTC time",
        "Timestamp (Unix Timestamp)",
        "UV Index (0-11+)",
        "Visibility (default KM)",
        "[icon: Weather icon code | code: Weather code | description: Text weather description.]",
        "Wind direction (degrees)",
        "Wind gust speed (Default m/s)",
        "Wind speed (Default m/s)"
    ]

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data['data'], columns=columns)

    df.columns = new_columns

    # Write DataFrame to Excel
    df.to_excel("Hourly_historical_weather_data.xlsx", index=False)

    print("Data written to Hourly_historical_weather_data.xlsx successfully.")
else:
    print("Failed to retrieve data. Status code:", response.status_code)
