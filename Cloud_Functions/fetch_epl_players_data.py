####################
# Import libraries #
####################

import requests
import pandas as pd
from google.cloud import storage
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


def fetch_countries_code_data(Request):
    data = []
    url = "https://api.sportmonks.com/v3/core/countries"
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
    countries_code_data = pd.DataFrame(data)

    # Selecting relevant columns to return
    columns_of_interest = ['id', 'continent_id', 'name', 'official_name', 'iso2', 'iso3']
    countries_code_data = countries_code_data[columns_of_interest].drop_duplicates().reset_index(drop=True)

    # Capture as csv
    #csv_countries_code_data = countries_code_data.to_csv(index=False)
    csv_countries_code_data = countries_code_data.to_csv(index=False, quoting=csv.QUOTE_NONNUMERIC)
    
    # Establish filename
    filename = f'countries_code_data.csv'

    # Create a client for the Google Cloud Storage
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket('countries_code_data')

    # Create a new blob (file) in the bucket
    blob = bucket.blob(filename)

    # Upload
    blob.upload_from_string(csv_countries_code_data, content_type='text/csv')
    
    return 'Countries code data CSV file written to bucket.'
    
