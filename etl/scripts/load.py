from pyspark.sql import SparkSession
import pandas as pd
import duckdb

def load_data(data, destination_type='parquet', destination_path='/etl/output/'):
    # Initialize Spark session
    spark = SparkSession.builder.appName("ETL_Load").getOrCreate()

    # Convert to Spark DataFrame if it's not already
    if isinstance(data, pd.DataFrame):
        df = spark.createDataFrame(data)
    else:
        df = data

    if destination_type == 'parquet':
        df.write.parquet(destination_path + 'output.parquet', mode='overwrite')
    
    elif destination_type == 'csv':
        df.write.csv(destination_path + 'output.csv', header=True, mode='overwrite')
    
    elif destination_type == 'json':
        df.write.json(destination_path + 'output.json', mode='overwrite')
    
    elif destination_type == 'database':
        # Example: writing to a PostgreSQL database
        df.write \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://localhost:5432/mydatabase") \
            .option("dbtable", "mytable") \
            .option("user", "username") \
            .option("password", "password") \
            .mode("overwrite") \
            .save()
    
    elif destination_type == 'duckdb':
        # Convert Spark DataFrame to Pandas for DuckDB
        pandas_df = df.toPandas()
        conn = duckdb.connect(destination_path + 'output.db')
        conn.execute("CREATE TABLE IF NOT EXISTS output_table AS SELECT * FROM pandas_df")
        conn.close()

    else:
        raise ValueError(f"Unsupported destination type: {destination_type}")

    print(f"Data successfully loaded to {destination_type} at {destination_path}")

# Additional utility functions
def partition_and_save(df, partition_column, destination_path):
    df.write.partitionBy(partition_column).parquet(destination_path, mode='overwrite')

def save_with_compression(df, destination_path, compression='snappy'):
    df.write.option("compression", compression).parquet(destination_path, mode='overwrite')