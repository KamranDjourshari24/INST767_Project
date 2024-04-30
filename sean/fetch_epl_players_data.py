####################
# Import libraries #
####################

import requests
from pandas import json_normalize
import pandas as pd
from google.cloud import storage
from datetime import datetime
import csv
import logging
import os


#########
# Setup #
#########

###
# Configure logging
###

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


###
# Define API key
###


###
# API endpoints
###


def fetch_epl_players_data(Request):
    data = []
    url = "https://api.sportmonks.com/v3/football/teams/seasons/21646?include=players.player"
    headers = {"Authorization": "ZsmqzVHh2cx0AcBaTlnKuV4Wh3XuYSlyYuh6yEDLULKpPa42fnbggIIubhNL", "Accept": "application/json"}
    pagination_key="pagination"

    while url:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            response_data = response.json()
            data.extend(response_data.get('data', []))

            if pagination_key in response_data and 'has_more' in response_data[pagination_key] and response_data[pagination_key]['has_more']:
                url = response_data[pagination_key].get('next_page', None)
                
            else:
                url = None
        except requests.HTTPError as e:
            logging.error(f"HTTP error occurred: {str(e)}")
            break
        except requests.RequestException as e:
            logging.error(f"Error during requests to {url}: {str(e)}")
            break

    # Transform to pandas dataframe        
    data_df = pd.DataFrame(data)

    # Create empty dataframe for holding players
    all_players = pd.DataFrame()


    # Loop through teams, extracting player data
    for idx, row in data_df.iterrows():
        if isinstance(row['players'], list):
            for player_data in row['players']:
                    # Normalize directly within the loop for each player data item
                player_details = json_normalize(player_data['player'])
                player_details['team_id'] = row['id']  # Assuming team 'id' should be linked with players

                    # Concatenate the normalized player details
                all_players = pd.concat([all_players, player_details], ignore_index=True)
    
    # Selecting relevant columns to return
    columns_of_interest = ['id', 'team_id', 'common_name', 'firstname', 'lastname', 'display_name', 'date_of_birth', 'country_id']
    all_players = all_players[columns_of_interest].drop_duplicates().reset_index(drop=True)

    # Capture as csv
    csv_epl_players_data = all_players.to_csv(index=False)

    # Establish filename
    filename = f'epl_players_data_{datetime.now()}.csv'

    # Create a client for the Google Cloud Storage
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket('epl_players_data')

    # Create a new blob (file) in the bucket
    blob = bucket.blob(filename)

    # Upload
    blob.upload_from_string(csv_epl_players_data, content_type='text/csv')
    
    
    return 'CSV file written to bucket.'
    
    