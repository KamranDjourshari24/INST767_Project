import requests
import pandas as pd

# Define the API endpoint
api_url = "https://api.openf1.org/v1/weather?meeting_key=1213"

# Fetch data from the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Convert response to JSON
    data = response.json()

    # Convert JSON data to DataFrame
    df = pd.DataFrame(data)

    # Save DataFrame to Excel file
    excel_file_path = "weather_data.xlsx"
    df.to_excel(excel_file_path, index=False)

    print("Data saved to:", excel_file_path)

else:
    print("Failed to fetch data from the API.")
