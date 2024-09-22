# Use the official Spark image as a base
FROM apache/spark:latest

USER root

# Install Python and pip if not already available
RUN apt-get update && apt-get install -y python3 python3-pip

# Install additional Python packages
RUN pip3 install --no-cache-dir \
    pandas \
    duckdb \
    pyarrow \
    pyspark \
    fastparquet \
    great_expectations \
    sqlalchemy \
    psycopg2-binary \
    requests

# Create directories for ETL operations
RUN mkdir -p /etl/input /etl/output /etl/scripts
RUN chown -R spark:spark /etl

# Switch back to the spark user
USER spark

# Set working directory
WORKDIR /etl

# Copy ETL scripts
COPY --chown=spark:spark scripts/ /etl/scripts/

# Print environment information for debugging
RUN echo "PATH: $PATH" && \
    echo "SPARK_HOME: $SPARK_HOME" && \
    ls -l $SPARK_HOME/bin && \
    which python3

# Use python to run the script instead of spark-submit for now
CMD ["python3", "/etl/scripts/main.py"]