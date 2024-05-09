from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, col

# Create a SparkSession
spark = SparkSession.builder.appName("f1_racer_country").getOrCreate()
spark = SparkSession.builder.getOrCreate()

# Read in the CSV files as Spark DataFrames
country_df = spark.read.csv("gs://countries_code_data/countries_code_data.csv", 
                            header=True, inferSchema=True)
driver_df = spark.read.csv("gs://f1_driver_data/f1_driver_data.csv", 
                           header=True, inferSchema=True)

# Clean data by converting NED to NLD for correct joining
driver_df = driver_df.withColumn("country_code", expr("CASE WHEN country_code "
                                                      "== 'NED' THEN 'NLD' "
                                                      "ELSE country_code END"))

# Join the two dataframes together
joined_df = country_df.join(driver_df, country_df.iso3 == driver_df.country_code
                            , "inner")

# Rename column and select columns needed
joined_df = joined_df.withColumnRenamed("name", 
                                        "country_name").select("driver_number", 
                                                               "full_name", 
                                                               "name_acronym", 
                                                               "first_name", 
                                                               "last_name", 
                                                               "country_name",
                                                               "iso3")

# Alias table columns with correct datatypes
joined_df = joined_df.select(
        col("driver_number").cast("integer").alias("Driver_Number"),
        col("full_name").alias("Full_Name"),
        col("first_name").alias("First_Name"),
        col("last_name").alias("Last_Name"),
        col("name_acronym").alias("Name_Acronym"),
        col("country_name").alias("Country"),
        col("iso3").alias("iso3")
)                                        

# Display joined dataframe
joined_df.show()


# Moving DataFrame to BigQuery
joined_df.write.format('bigquery') \
    .option('writeMethod', 'direct') \
    .option('table', 'inst767-419822.finalproject.racerf1_country') \
    .option('temporaryGcsBucket', '767-temp') \
    .mode('overwrite') \
    .save()

# SparkSession Stopped
spark.stop()