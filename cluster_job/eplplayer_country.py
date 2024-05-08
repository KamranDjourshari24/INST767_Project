from pyspark.sql import SparkSession
from pyspark.sql.functions import substring, col, to_date

# Creating Spark Session & Reading in necessary data
spark = SparkSession.builder.appName("epl_players").getOrCreate()
country_df = spark.read.format("csv") \
                  .option("header", "true") \
                  .load("gs://countries_code_data/countries_code_data_"
                        "2024-04-30 16:35:36.535473.csv")
epl_df = spark.read.format("csv") \
              .option("header", "true") \
              .load("gs://epl_players_data/epl_players_"
                    "data_2024-04-30 14:25:17.543472.csv")

joined_df = country_df.join(epl_df, country_df.id == epl_df.country_id, "left")

joined_df = joined_df.withColumnRenamed("name", "country_name") \
                     .select("display_name", "firstname", "lastname",
                             "date_of_birth","country_name", "iso3")

# Remove nulls from the joined_df
joined_df = joined_df.dropna()

# Create a year column using the date_of_birth column
joined_df = joined_df.withColumn("birth_year", substring("date_of_birth", 1, 4))

# Alias table columns with correct datatypes
joined_df = joined_df.select(
        col("display_name").alias("display_name"),
        col("firstname").alias("firstname"),
        col("lastname").alias("lastname"),
        to_date(col("date_of_birth")).alias("date_of_birth"),
        col("country_name").alias("country_name"),
        col("iso3").alias("iso3"),
        col("birth_year").cast('integer').alias("birth_year")
)

# Show the joined_df with the new year column
joined_df.show()

# Moving DataFrame to Bigquery
joined_df.write.format('bigquery') \
    .option('writeMethod', 'direct') \
    .option('table', 'inst767-419822.finalproject.epl_country') \
    .option('temporaryGcsBucket', 'epl-temp') \
    .mode('overwrite') \
    .save()

# SparkSession Stopped
spark.stop()