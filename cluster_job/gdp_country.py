from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, col

# Create a SparkSession
spark = SparkSession.builder.appName("gdp_country").getOrCreate()
spark = SparkSession.builder.getOrCreate()

# Read in datasets as PySpark Dataframes
country_df = spark.read.csv("gs://countries_code_data/countries_code_data.csv", 
                            header=True, inferSchema=True)
gdp_df = spark.read.csv("gs://gdp_bank/gdp_data.csv", header=True, 
                        inferSchema=True)

# Join the two dataframes together
joined_df = country_df.join(gdp_df, country_df.iso3 == gdp_df.Country_code
                            ,"right")

# Alias table columns with correct datatypes
joined_df = joined_df.select(
        col("Country_code").alias("Country_Code"),
        col("name").alias("Country_Name"),
        col("Value").alias("GDP_Value"),
        col("Year").cast('integer').alias("Year"),
        col("GDP_Change_Rate").cast('double').alias("GDP_Change_Rate")
) 

# Display joined dataframe
joined_df.show()


# Moving DataFrame to BigQuery
joined_df.write.format('bigquery') \
    .option('writeMethod', 'direct') \
    .option('table', 'inst767-419822.finalproject.gdp_country') \
    .option('temporaryGcsBucket', '767-temp') \
    .mode('overwrite') \
    .save()

# SparkSession Stopped
spark.stop()