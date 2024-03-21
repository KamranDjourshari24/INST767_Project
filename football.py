import requests

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

# Replace 'your_api_key_here' with your actual Sportmonks API key
api_key = "mfou7aOZmxw5Y0DBa772xTs0rkIreQ8Y1zt7oWD9Gnu9uPT4ZUW0NXkBlBXy"
leagues_data = get_leagues(api_key)
if leagues_data:
    print(leagues_data)
