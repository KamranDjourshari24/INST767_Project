# -*- coding: utf-8 -*-

!pip install pyspark

import pyspark
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.appName("Example").getOrCreate()

# Read in the CSV files as Spark DataFrames
race_df = spark.read.csv("/content/F1_race_2024-05-02 18_37_43.479007.csv", header=True)
gdp_df = spark.read.csv("/content/gdp_data_2024-04-30 20_09_34.138179.csv", header=True)
country_df = spark.read.csv("/content/countries_code_data_2024-04-30 16_35_36.535473 (1).csv", header=True)

#
country_df.show()
gdp_df.show()
race_df.show()

from pyspark.sql import functions as F

race_df = race_df.withColumn("Country",
                               F.when(race_df.Country == "UK", "England")
                               .when(race_df.Country == "USA", "United States")
                               .when(race_df.Country == "Korea", "South Korea")
                               .when(race_df.Country == "UAE", "United Arab Emirates")
                               .otherwise(race_df.Country))

race_df.show()

race_country_df = race_df.join(country_df, race_df.Country == country_df.name, "inner")
