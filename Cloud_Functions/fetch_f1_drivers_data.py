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

# Function to grab F1 driver stats
def fetch_f1_driver_data(Request):
    
    base_url = "https://api.openf1.org/v1/drivers?session_key=7763"

    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        response_data = response.json()  # No need to convert to JSON as requests handles this
        
        # Convert directly to a DataFrame
        data_df = pd.DataFrame(response_data)
    except requests.HTTPError as e:
        logging.error(f"HTTP error occurred: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while fetching F1 data: {str(e)}")
        return None


    # Capture as csv
    f1_driver_data = data_df.to_csv(index=False)

    # Establish filename
    filename = f'f1_driver_data.csv'

    # Create a client for the Google Cloud Storage
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket('f1_driver_data')

    # Create a new blob (file) in the bucket
    blob = bucket.blob(filename)

    # Upload
    blob.upload_from_string(f1_driver_data, content_type='text/csv')
    
    return 'f1 driver data CSV file written to bucket.'
