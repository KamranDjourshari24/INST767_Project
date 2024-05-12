# INST767 Project: F1 Racing and EPL Data with Country GDP Pipeline

## Group 9: Kamran Djourshari, Steicy Singh, Saran Ram, Sean Mussenden, Angela Tseng, Hrday Kowdley

## Introduction
For this project, we focused on various aspects to ensure a smooth functioning 
data-pipeline. The topic we chose to cover was F1 Racing and the English Premier
League (EPL) Football relation to GDP of countries, using Racers and
players' ethnicities. This was broken into 4 different steps, which 
will be covered here. These four steps include ingestion, transformation, 
storage and analysis. For this to occur we used Google Cloud to create this 
project. 


## Ingestion
For this step, we conducted this using five different Cloud Functions which call
from these different free open-sourced APIs. Each of these Cloud Functions store
their data into their own seperate intermediate cloud storage Google Bucket as
.csv files.
!["Picture of all 5 Cloud Functions"](images/cloud_functions_success.png)

Below are all of our functioning Google Cloud Functions with a brief summary of
their API source and code:

1. **Cloud_Functions/fl_data**: This code pulls data from Ergast API, which 
    contains information about all the Formula 1 Races. Our code pulls in all 
    the races starting from 2005 (the earliest the API allows for) all the way 
    to the current year (using the Datatime Module), which allows for our code 
    to remain dynamic no matter what year it is. Once gathered, it sends all the
    data to the ***f1_race_info*** bucket.
    !["Bucket with CSV"](images/f1_race_bucket.png)

2. **Cloud_Functions/fetch_countries_code_data.py**: Pulling data from the 
    SportsMonk API source, this returns all the Countries information (id, name, 
    iso2, iso3 code). It stores the data in the ***countries_code_data*** 
    bucket.
    !["Bucket with CSV"](images/countries_bucket.png)

3. **Cloud_Functions/fetch_epl_players_data.py**: This also pulls data from the 
    SportsMonk API source for English Premier League Players, including their 
    name, country of origin and date of birth. The data is then stored in the 
    ***epl_players_data*** bucket.
    !["Bucket with CSV"](images/epl_bucket.png)   
    
4. **Cloud_Functions/fetch_f1_drivers_data.py**: This retrieves data from the 
    SportsMonk API source for F1 Drivers in current races also, including their 
    name, country of origin and date of birth. The data is then stored in the 
    ***f1_driver_data*** bucket.   
    !["Bucket with CSV"](images/f1_driver_bucket.png)

5. **Cloud_Functions/get_gdp_data.py**: Pulling data from the World Bank and 
    IMF APIs we are able to pull in all countries GDP data (value and change 
    rate) starting from 1980 to present time. NOTE: We had to pull from two 
    different APIs as the World Bank API doesn't return GDP data of all
    countries from one query/API call. Instead we had to query each country with 
    the World Bank API and pull the necessary data. We were able to query by 
    each country by using the IMFs API which returns all country names. The data 
    is then stored in the ***gdp_bank*** bucket.
    !["Bucket with CSV"](images/gdp_bucket.png)    