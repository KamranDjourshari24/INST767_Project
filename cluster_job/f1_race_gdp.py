from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import col, to_date, substring, concat, lit

# Create a SparkSession
spark = SparkSession.builder.appName("f1_race").getOrCreate()

# Read in the CSV files as Spark DataFrames
race_df = spark.read.csv("gs://f1_race_info/F1_race.csv", header=True)
gdp_df = spark.read.csv("gs://gdp_bank/gdp_data.csv", header=True)
country_df = spark.read.csv("gs://countries_code_data/countries_code_data.csv", 
                            header=True)

# Cleaning data so the joins can be done with country name 
race_df = race_df.withColumn("Country",
                               F.when(race_df.Country == "UK", "England")
                               .when(race_df.Country == "USA", "United States")
                               .when(race_df.Country == "Korea", "South Korea")
                               .when(race_df.Country == "UAE", 
                                     "United Arab Emirates")
                               .otherwise(race_df.Country))

# Joining race data with country
race_country_df = race_df.join(country_df, race_df.Country == country_df.name, 
                               "inner")

race_country_df = race_country_df.withColumn("Time", substring("Time", 1, 11))

# Combine date and time (string format)
combined_datetime = concat(col("Date"), lit(" "), col("Time"))

race_country_df = race_country_df.withColumn("datetime", combined_datetime.alias("combined_datetime"))

# Alias table columns with correct datatypes
race_country_df = race_country_df.select(
        col("Race Name").alias("Race_Name"),
        col("datetime").cast('timestamp').alias("DateTime"),
        col("Circuit").alias("Circuit"),
        col("Location").alias("City"),
        col("Country").alias("Country"),
        col("Year").cast('integer').alias("Year"),
        col("iso3").alias("iso3")
)

# Show the race_country_df
race_country_df.show()

# Moving DataFrame to BigQuery
race_country_df.write.format('bigquery') \
    .option('writeMethod', 'direct') \
    .option('table', 'inst767-419822.finalproject.f1_race') \
    .option('temporaryGcsBucket', '767-temp') \
    .mode('overwrite') \
    .save()

# SparkSession Stopped
spark.stop()
