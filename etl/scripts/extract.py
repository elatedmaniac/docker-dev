import pandas as pd
from pyspark.sql import SparkSession
import requests
import json
import sqlalchemy
import duckdb
import pyarrow.parquet as pq

def extract_data(source_type, source_path=None, **kwargs):
    """
    Extract data from various sources.
    
    :param source_type: Type of data source ('csv', 'parquet', 'json', 'database', 'api', 'duckdb')
    :param source_path: Path or URL of the data source
    :param kwargs: Additional arguments specific to each source type
    :return: DataFrame (Pandas or PySpark)
    """
    
    if source_type == 'csv':
        return extract_from_csv(source_path, **kwargs)
    elif source_type == 'parquet':
        return extract_from_parquet(source_path, **kwargs)
    elif source_type == 'json':
        return extract_from_json(source_path, **kwargs)
    elif source_type == 'database':
        return extract_from_database(**kwargs)
    elif source_type == 'api':
        return extract_from_api(source_path, **kwargs)
    elif source_type == 'duckdb':
        return extract_from_duckdb(source_path, **kwargs)
    else:
        raise ValueError(f"Unsupported source type: {source_type}")

def extract_from_csv(file_path, use_spark=False, **kwargs):
    if use_spark:
        spark = SparkSession.builder.appName("ETL_Extract").getOrCreate()
        return spark.read.csv(file_path, header=True, inferSchema=True)
    else:
        return pd.read_csv(file_path, **kwargs)

def extract_from_parquet(file_path, use_spark=False, **kwargs):
    if use_spark:
        spark = SparkSession.builder.appName("ETL_Extract").getOrCreate()
        return spark.read.parquet(file_path)
    else:
        return pd.read_parquet(file_path, **kwargs)

def extract_from_json(file_path, use_spark=False, **kwargs):
    if use_spark:
        spark = SparkSession.builder.appName("ETL_Extract").getOrCreate()
        return spark.read.json(file_path)
    else:
        return pd.read_json(file_path, **kwargs)

def extract_from_database(connection_string, query, **kwargs):
    engine = sqlalchemy.create_engine(connection_string)
    return pd.read_sql(query, engine, **kwargs)

def extract_from_api(api_url, params=None, headers=None):
    response = requests.get(api_url, params=params, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    return pd.DataFrame(data)

def extract_from_duckdb(db_path, query):
    conn = duckdb.connect(db_path)
    result = conn.execute(query).fetchdf()
    conn.close()
    return result

# Additional utility functions

def list_parquet_files(directory):
    """List all Parquet files in a directory."""
    return [f for f in os.listdir(directory) if f.endswith('.parquet')]

def sample_large_dataset(file_path, sample_size=1000, use_spark=True):
    """Sample a large dataset."""
    if use_spark:
        spark = SparkSession.builder.appName("ETL_Extract_Sample").getOrCreate()
        full_data = spark.read.parquet(file_path)
        return full_data.sample(False, sample_size / full_data.count())
    else:
        return pq.read_table(file_path).to_pandas().sample(n=sample_size)

def extract_from_multiple_sources(source_configs):
    """
    Extract data from multiple sources and combine them.
    
    :param source_configs: List of dictionaries, each containing 'type', 'path', and other necessary parameters
    :return: Combined DataFrame
    """
    dataframes = []
    for config in source_configs:
        df = extract_data(config['type'], config.get('path'), **config.get('params', {}))
        dataframes.append(df)
    
    # Combine dataframes - this is a simple concatenation, adjust as needed
    return pd.concat(dataframes, ignore_index=True)

# Example usage
if __name__ == "__main__":
    # Example: Extract from CSV
    csv_data = extract_data('csv', '/path/to/data.csv')
    
    # Example: Extract from API
    api_data = extract_data('api', 'https://api.example.com/data', params={'key': 'value'})
    
    # Example: Extract from multiple sources
    configs = [
        {'type': 'csv', 'path': '/path/to/data1.csv'},
        {'type': 'parquet', 'path': '/path/to/data2.parquet'},
        {'type': 'database', 'params': {
            'connection_string': 'postgresql://user:password@localhost/dbname',
            'query': 'SELECT * FROM table'
        }}
    ]
    combined_data = extract_from_multiple_sources(configs)
    
    print(f"CSV data shape: {csv_data.shape}")
    print(f"API data shape: {api_data.shape}")
    print(f"Combined data shape: {combined_data.shape}")