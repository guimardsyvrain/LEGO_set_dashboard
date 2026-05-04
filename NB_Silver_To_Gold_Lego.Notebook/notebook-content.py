# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "32c54c98-b8a0-4cea-b9e2-3020539581c6",
# META       "default_lakehouse_name": "LH_Silver_Lego",
# META       "default_lakehouse_workspace_id": "d41978dc-b7f2-446f-a482-c56bfa049e3d",
# META       "known_lakehouses": [
# META         {
# META           "id": "32c54c98-b8a0-4cea-b9e2-3020539581c6"
# META         },
# META         {
# META           "id": "19940900-5365-4e7b-82fd-f74c60bcd676"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # This notebook is used to break down the dataset into fact and dimension tables.

# MARKDOWN ********************

# ### 1. Importing required modules

# CELL ********************

import pandas as pd
import numpy as np
import requests
from pyspark.sql.functions import col, when

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 2. Importing the dataset from Silver Lakehouse

# CELL ********************

# Read the enriched "lego_sets" dataset.

# Path to access "lego_sets" into Lego Silver lakehouse  
lego_silver_path = "abfss://Lego_set_Report@onelake.dfs.fabric.microsoft.com/LH_Silver_Lego.Lakehouse/Tables/dbo/lego_sets_cleaned3"

# Load the lego dataset into a dataframe
lego_sets_cleaned3 = spark.read.format("delta").load(lego_silver_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(lego_sets_cleaned3)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Displaying the columns name
lego_sets_cleaned3.columns

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 3. Generating the "age group" and "price range" variables.

# CELL ********************

lego_sets_final = lego_sets_cleaned3.withColumn("age_group", when(col("agerange_min") > 18, "Over 18")\
                                    .when(col("agerange_min") > 9, "[10 - 17]")\
                                    .when(col("agerange_min") > 4, "[5 - 9]")\
                                    .otherwise("[1 - 4]"))\
                                    .withColumn("price_range", when(col("US_retailPrice") > 500, ">500$")\
                                    .when(col("US_retailPrice") > 100, ">100$")\
                                    .when(col("US_retailPrice") > 50, ">50$")\
                                    .when(col("US_retailPrice") > 25, ">25$")\
                                    .otherwise("less than 25$"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 4. Generating the dimension table from "lego_sets_final" dataset.

# CELL ********************

# Create a temporary table using sql
lego_sets_final.createOrReplaceTempView("lego_sets_final")

# Select the needed table from lego_sets_cleaned3 using Spark SQL
lego_dim = spark.sql("""
SELECT 
    set_id,
    name,
    year,
    theme,
    subtheme,
    themeGroup,
    category,
    agerange_min,
    age_group,
    price_range,
    imageURL
FROM lego_sets_final
""")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 5. Generating the fact table extracted from "lego_sets_final" dataset.

# CELL ********************

# Create a temporary table using sql
lego_sets_final.createOrReplaceTempView("lego_sets_final")

# Select the needed table from lego_sets_cleaned3 using Spark SQL
lego_fact = spark.sql("""
SELECT 
    set_id,
    pieces,
    US_retailPrice
FROM lego_sets_final
""")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 6. Save the two datasets into the gold Lakehouse

# CELL ********************

# Save lego_dim table as a dataframe into the gold lakehouse
lego_dim_gold_path = "abfss://Lego_set_Report@onelake.dfs.fabric.microsoft.com/LH_Gold_Lego.Lakehouse/Tables/dbo/lego_dim"
lego_dim.write.format("delta").mode("overwrite").save(lego_dim_gold_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Save lego_fact table as a dataframe 
lego_fact_gold_path= "abfss://Lego_set_Report@onelake.dfs.fabric.microsoft.com/LH_Gold_Lego.Lakehouse/Tables/dbo/lego_fact"
lego_fact.write.format("delta").mode("overwrite").save(lego_fact_gold_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
