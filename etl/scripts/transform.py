import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, to_date
import great_expectations as ge

def transform_data(data):
    # Initialize Spark session
    spark = SparkSession.builder.appName("ETL_Transform").getOrCreate()

    # Convert to Spark DataFrame if it's not already
    if isinstance(data, pd.DataFrame):
        df = spark.createDataFrame(data)
    else:
        df = data

    # Data cleaning
    df = df.dropDuplicates()
    df = df.na.fill({"numeric_column": 0, "string_column": "Unknown"})

    # Data type conversions
    df = df.withColumn("date_column", to_date(col("date_column")))

    # Feature engineering
    df = df.withColumn("new_feature", when(col("condition_column") > 10, 1).otherwise(0))

    # Aggregations
    df_agg = df.groupBy("category_column").agg({"value_column": "sum"})

    # Join operations
    df_joined = df.join(df_agg, "category_column", "left")

    # Data validation with Great Expectations
    ge_df = ge.dataset.SparkDFDataset(df_joined)
    validation_result = ge_df.expect_column_values_to_be_between("value_column", min_value=0, max_value=1000)

    if not validation_result.success:
        print("Data validation failed:", validation_result)

    return df_joined

# Additional utility functions can be added here
def normalize_column_names(df):
    return df.select([col(c).alias(c.lower().replace(' ', '_')) for c in df.columns])

def categorize_values(df, column_name, bins, labels):
    return df.withColumn(f"{column_name}_category", 
                         pd.cut(col(column_name), bins=bins, labels=labels))