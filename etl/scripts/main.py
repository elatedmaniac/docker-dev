import os
import sys

print("Python version:", sys.version)
print("Current working directory:", os.getcwd())
print("Contents of current directory:", os.listdir('.'))
print("Contents of /etl/scripts:", os.listdir('/etl/scripts'))
print("PATH:", os.environ.get('PATH'))
print("SPARK_HOME:", os.environ.get('SPARK_HOME'))

try:
    from pyspark.sql import SparkSession
    print("PySpark imported successfully")
except ImportError as e:
    print("Failed to import PySpark:", e)

def main():
    try:
        # Try to create a local Spark session
        spark = SparkSession.builder.appName("ETL_Pipeline").master("local[*]").getOrCreate()
        print("Spark session created successfully")
        
        # Your ETL logic here
        # For now, just print some information about the Spark session
        print("Spark version:", spark.version)
        print("Spark configuration:", spark.sparkContext.getConf().getAll())
        
        # Stop Spark session
        spark.stop()
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()