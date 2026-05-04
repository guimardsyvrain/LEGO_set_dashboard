# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "b4a02cec-5f69-46bf-858b-fa97b39d6041",
# META       "default_lakehouse_name": "LH_Bronze_Lego",
# META       "default_lakehouse_workspace_id": "d41978dc-b7f2-446f-a482-c56bfa049e3d",
# META       "known_lakehouses": [
# META         {
# META           "id": "b4a02cec-5f69-46bf-858b-fa97b39d6041"
# META         },
# META         {
# META           "id": "32c54c98-b8a0-4cea-b9e2-3020539581c6"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # This notebook is used for data exploratory analysis and cleaning tasks to enrich the dataset for analytics and reporting purposes.

# MARKDOWN ********************

# ### 1. Importing all required module from python

# CELL ********************

import pandas as pd
import numpy as np
import requests
from pyspark.sql.functions import col

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 2. Loading the dataset

# CELL ********************

# Path to access "lego_sets" into Lego Lakehouse bronze 
lego_bronze_path = "abfss://Lego_set_Report@onelake.dfs.fabric.microsoft.com/LH_Bronze_Lego.Lakehouse/Tables/dbo/lego_sets"

# Load the lego dataset into a dataframe
lego_sets = spark.read.format("delta").load(lego_bronze_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 3. Checking on the dimension of the dataset and statistics.

# CELL ********************

# Printing out the dataset structure
row_count = lego_sets.count()
col_count = len(lego_sets.columns)

print(f"The dimensions of the dataset are: {row_count} rows and {col_count} columns")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Printing out a descriptive summary table of the dataset
display(lego_sets.describe())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 4. Clean the datasets for analytics

# CELL ********************

# Removing the following columns 'minifigs', 'bricksetURL', 'thumbnailURL' from the dataset
lego_sets_cleaned1 = lego_sets.drop('minifigs', 'bricksetURL', 'thumbnailURL')

# Filtering out records with no price, age, pieces or image URL values
lego_sets_cleaned2 = lego_sets_cleaned1.filter(col('US_retailPrice').isNotNull() &
                                               col('agerange_min').isNotNull() &
                                               col('pieces').isNotNull()
   )

# Filtering out records with no image URL values
lego_sets_cleaned3 = lego_sets_cleaned2.dropna(subset = "imageURL") 

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Output the enriched lego_set dataset
row_count3 = lego_sets_cleaned3.count()
col_count3 = len(lego_sets_cleaned3.columns)

print(f"The dimensions of the enriched lego_set are: {row_count3} rows and {col_count3} columns")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 5. Save datasets into the Silver Lakehouse

# CELL ********************

# Save the lego_sets_cleaned3 into the silver lakehouse
lego_silver_path = 'abfss://Lego_set_Report@onelake.dfs.fabric.microsoft.com/LH_Silver_Lego.Lakehouse/Tables/dbo/lego_sets_cleaned3'
lego_sets_cleaned3.write.format("delta").mode("overwrite").save(lego_silver_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
