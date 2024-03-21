import requests
import csv

def get_leagues(api_key):
    url = "https://soccer.sportmonks.com/api/v2.0/leagues"
    headers = {
        "Accept": "application/json",
    }
    params = {
        "api_token": api_key,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def write_leagues_to_csv(leagues_data, filename):
    # Assuming leagues_data['data'] is the list of leagues
    leagues = leagues_data.get('data', [])
    if leagues:
        # Define the CSV column names (adjust these based on the actual data structure)
        fieldnames = ['id', 'name', 'country_id', 'is_cup']
        
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for league in leagues:
                # Adjust the row dict if the structure of league objects is different
                row = {fieldname: league.get(fieldname, '') for fieldname in fieldnames}
                writer.writerow(row)
    else:
        print("No leagues data to write.")

# Replace 'your_api_key_here' with your actual Sportmonks API key
api_key = "mfou7aOZmxw5Y0DBa772xTs0rkIreQ8Y1zt7oWD9Gnu9uPT4ZUW0NXkBlBXy"
leagues_data = get_leagues(api_key)
if leagues_data:
    write_leagues_to_csv(leagues_data, 'leagues.csv')
    print("Leagues data has been written to leagues.csv")
