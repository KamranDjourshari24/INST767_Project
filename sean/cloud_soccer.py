
####################
# Import libraries #
####################

import requests
import pandas as pd
import logging
from pandas import json_normalize
import geopandas
import matplotlib
import contextily
import geopandas as gpd
import matplotlib.pyplot as plt

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

headers = {"Authorization": "ZsmqzVHh2cx0AcBaTlnKuV4Wh3XuYSlyYuh6yEDLULKpPa42fnbggIIubhNL", "Accept": "application/json"}

###
# API endpoints
###

# Sportsmonks
soccer_base_url = "https://api.sportmonks.com/v3/football/teams/seasons/21646?include=players.player"
countries_base_url = "https://api.sportmonks.com/v3/core/countries"

# OpenF1
f1_base_url = "https://api.openf1.org/v1/drivers?session_key=7763"

####################
# Define functions #
####################

###
# Function to fetch data from sportsmonks football/soccer API endpoints
###

def fetch_sportsmonks_data(base_url, headers, pagination_key="pagination", only_first_page=False, is_team_players=False):
    data = []
    url = base_url

    while url:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            response_data = response.json()
            data.extend(response_data.get('data', []))

            if pagination_key in response_data and 'has_more' in response_data[pagination_key] and response_data[pagination_key]['has_more']:
                url = response_data[pagination_key].get('next_page', None)
                if only_first_page:
                    break
            else:
                url = None
        except requests.HTTPError as e:
            logging.error(f"HTTP error occurred: {str(e)}")
            break
        except requests.RequestException as e:
            logging.error(f"Error during requests to {url}: {str(e)}")
            break

    data_df = pd.DataFrame(data)
    if is_team_players and not data_df.empty:
        return extract_players_info(data_df)
    else:
        return data_df
      
###
# Function to transform player data
###

def extract_players_info(data_df):
    all_players = pd.DataFrame()

    if 'players' in data_df.columns:
        for idx, row in data_df.iterrows():
            if isinstance(row['players'], list):
                for player_data in row['players']:
                    # Normalize directly within the loop for each player data item
                    player_details = json_normalize(player_data['player'])
                    player_details['team_id'] = row['id']  # Assuming team 'id' should be linked with players

                    # Concatenate the normalized player details
                    all_players = pd.concat([all_players, player_details], ignore_index=True)

    # Selecting relevant columns to return
    if not all_players.empty:
        columns_of_interest = ['id', 'team_id', 'common_name', 'firstname', 'lastname', 'display_name', 'date_of_birth', 'country_id']
        return all_players[columns_of_interest].drop_duplicates().reset_index(drop=True)
    else:
        return pd.DataFrame()

def process_team_and_country_data(teams_df, countries_df):
    """
    Processes team and country data to merge, aggregate, and calculate statistics.
    
    Args:
    teams_df (pd.DataFrame): DataFrame containing team player data with 'country_id'.
    countries_df (pd.DataFrame): DataFrame containing country data with 'country_id', 'country_name', and 'iso3'.
    
    Returns:
    pd.DataFrame: Summary DataFrame with player counts and percentages by country.
    """
    # Ensure the country_id is in string format for both DataFrames
    teams_df['country_id'] = teams_df['country_id'].astype(str)
    countries_df['country_id'] = countries_df['country_id'].astype(str)
    
    # Perform a left join with the countries DataFrame
    merged_df = teams_df.merge(
        countries_df,
        how='left',
        on='country_id'
    )

    # Group by country and count the number of players, then calculate percentages
    summary_df = merged_df.groupby(['country_name', 'iso3']) \
        .size() \
        .reset_index(name='pl_players_count') \
        .sort_values('pl_players_count', ascending=False)

    # Calculate the percentage of players from each country
    total_players = summary_df['pl_players_count'].sum()
    summary_df['pl_players_pct'] = (summary_df['pl_players_count'] / total_players * 100).round(2)

    # Rename 'iso3' column to 'country_code' and ensure it is a string
    summary_df = summary_df.rename(columns={'iso3': 'country_code'})
    summary_df['country_code'] = summary_df['country_code'].astype(str)

    return summary_df

# Function to grab F1 driver stats
def fetch_f1(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        response_data = response.json()  # No need to convert to JSON as requests handles this
        
        # Convert directly to a DataFrame
        data_df = pd.DataFrame(response_data)
        return data_df
    except requests.HTTPError as e:
        logging.error(f"HTTP error occurred: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"An error occurred while fetching F1 data: {str(e)}")
        return None


def merge_pl_summary_with_f1(summary_df, f1_stats_df):
    try:
        # Perform a left join between the summary DataFrame and the F1 statistics DataFrame
        combined_df = summary_df.merge(f1_stats_df, how='left', left_on='country_code', right_on='country_code')
        logging.info("Successfully merged player team summary with F1 driver statistics.")
        return combined_df
    except Exception as e:
        logging.error(f"An error occurred while merging player team summary with F1 driver statistics: {str(e)}")
        return None
###
# Function to calculate f1 driver stats
###

def calculate_f1_driver_statistics(f1_data_df):
    try:
        # Assuming there's a 'country_code' column in the fetched F1 data
        # Group by 'country_code', count the drivers, sort, and calculate percentage
        f1_driver_stats = f1_data_df.groupby('country_code') \
            .size() \
            .reset_index(name='f1_driver_count') \
            .sort_values('f1_driver_count', ascending=False) \
            .reset_index(drop=True)
        
        total_drivers = f1_driver_stats['f1_driver_count'].sum()
        f1_driver_stats['f1_driver_pct'] = (f1_driver_stats['f1_driver_count'] / total_drivers * 100).round(2)
        
        return f1_driver_stats
    except Exception as e:
        logging.error(f"An error occurred while calculating F1 driver statistics: {str(e)}")
        return None

############
# Get Data #
############


###
# Get current season PL players from sportsmonks
###
 
try:
   
    current_pl_teams_w_players = fetch_sportsmonks_data(soccer_base_url, headers, only_first_page=False, is_team_players=True)

except Exception as e:
  
    logging.error(f"An error occurred: {str(e)}")
    

###
# Fetch countries data from sportsmonks
###
    
try:

    all_countries_df = fetch_sportsmonks_data(countries_base_url, headers, only_first_page=False)
    
    # Perform selection and type conversion
    if 'iso3' in all_countries_df.columns:
        all_countries_df = all_countries_df[['id', 'name', 'iso3']]
        all_countries_df = all_countries_df.rename(columns={'id': 'country_id', 'name': 'country_name'})
        all_countries_df['country_id'] = all_countries_df['country_id'].astype(str)
    
    logging.info("Fetched and processed country data successfully.")
except Exception as e:
    logging.error(f"An error occurred while fetching and processing country data: {str(e)}")  

###
# Combine Sportsmonks Soccer and Country data
###

try:
   
   summary_pl_teams = process_team_and_country_data(current_pl_teams_w_players, all_countries_df)
   logging.info("Merged team players with country data and created summary successfully.")
    
except Exception as e:
    logging.error(f"An error occurred while merging team players with country data: {str(e)}")
  


# Usage

try:
    f1_data_df = fetch_f1(f1_base_url)
    
    if f1_data_df is not None:
        f1_driver_stats_df = calculate_f1_driver_statistics(f1_data_df)
        if f1_driver_stats_df is not None:
            logging.info("F1 driver statistics calculated successfully.")
            # Now you can use 'f1_driver_stats_df' for further processing
        else:
            logging.error("Failed to calculate F1 driver statistics.")
    else:
        logging.error("Failed to fetch F1 data.")

except Exception as e:
    logging.error(f"An error occurred during the F1 data fetching and statistics calculation process: {str(e)}")



try:
    # Assuming 'summary_pl_teams' and 'f1_driver_stats_df' are defined and populated DataFrames from earlier steps
    compare_df = merge_pl_summary_with_f1(summary_pl_teams, f1_driver_stats_df)
    if compare_df is not None:
        # Continue with additional processing or analysis using 'compare_df'
        logging.info("The merged DataFrame is ready for further analysis.")
    else:
        logging.error("The DataFrame merge was unsuccessful.")
except Exception as e:
    logging.error(f"An error occurred while executing the merge operation: {str(e)}")
    
###
# Viz
###
 
try:
    # Load world map
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # Ensure the country code in world and df are of the same type
    world['iso_a3'] = world['iso_a3'].astype(str)
    compare_df['country_code'] = compare_df['country_code'].astype(str)

    # Filter out England from compare_df
    compare_df_no_england = compare_df[compare_df['country_name'] != 'England']
  
    # Merge the world map with your data
    merged = world.merge(compare_df_no_england, left_on='iso_a3', right_on='country_code', how='left')
  
    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged.boundary.plot(ax=ax)
    merged.plot(column='pl_players_pct', ax=ax, legend=True,
                legend_kwds={'label': "Player Percentage by Country",
                             'orientation': "horizontal"})
    plt.title('Choropleth Map Showing Player Percentages')
    plt.show()
except Exception as e:
    print(f"An error occurred: {e}")
    
    
try:
  
    # Load world map
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    
    european_countries = [
    'ALB', 'AND', 'AUT', 'BLR', 'BEL', 'BIH', 'BGR', 'HRV', 'CYP', 'CZE',
    'DNK', 'EST', 'FIN', 'FRA', 'DEU', 'GRC', 'HUN', 'ISL', 'IRL', 'ITA',
    'XKX', 'LVA', 'LIE', 'LTU', 'LUX', 'MLT', 'MDA', 'MCO', 'MNE', 'NLD',
    'MKD', 'NOR', 'POL', 'PRT', 'ROU', 'SMR', 'SRB', 'SVK', 'SVN',
    'ESP', 'SWE', 'CHE', 'UKR', 'VAT'
]

    # Filter for only European countries
    europe = world[world['iso_a3'].isin(european_countries)]
    
    # Ensure the country code in europe and compare_df are of the same type
    europe['iso_a3'] = europe['iso_a3'].astype(str)
    compare_df['country_code'] = compare_df['country_code'].astype(str)

    # Filter out England from compare_df if still needed
    compare_df = compare_df[compare_df['country_name'] != 'England']
  
    # Merge the European map with your data
    merged = europe.merge(compare_df, left_on='iso_a3', right_on='country_code', how='left')
  
    # Plotting
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    ax.set_xlim(-10, 40)  # Adjust these limits to better fit the visualization you need
    ax.set_ylim(35, 70)
    merged.boundary.plot(ax=ax)
    merged.plot(column='pl_players_pct', ax=ax, legend=True,
                legend_kwds={'label': "Player Percentage by Country",
                             'orientation': "horizontal"})
    plt.title('Choropleth Map of Europe Showing Player Percentages, No England')
    plt.show()
except Exception as e:
    print(f"An error occurred: {e}")
    
    


# Step 1: Filter out rows where 'f1_driver_pct' is NaN
filtered_df = compare_df.dropna(subset=['f1_driver_pct'])

filtered_df['country_name'] = filtered_df['country_name'].replace('United States', 'United\nStates')

# Step 2: Sort the DataFrame by 'f1_driver_pct' in descending order
sorted_df = filtered_df.sort_values(by='f1_driver_pct', ascending=False)

# Step 3: Plotting a horizontal bar chart
plt.figure(figsize=(12, 8))
plt.barh(sorted_df['country_name'], sorted_df['f1_driver_pct'], color='b')
plt.xlabel('F1 Driver Percentage')
plt.title('F1 Driver Percentages by Country')
plt.gca().invert_yaxis()  # Invert y-axis to have the highest percentage at the top
plt.tight_layout()  # Adjust layout to make room for the labels
plt.show()
