FROM apache/airflow:2.7.1

USER root

# Install any additional system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch back to the airflow user
USER airflow

RUN pip install --upgrade pip

# Install any additional Python packages your DAGs might need
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark \
    requests \
    pandas

# Copy DAGs
COPY --chown=airflow:root dags /opt/airflow/dags

ENV AIRFLOW_HOME=~/airflow

# install from pypi using pip
RUN pip install apache-airflow

# initialize the database
RUN airflow db init



# Set the entrypoint to run the Airflow webserver
ENTRYPOINT ["airflow", "webserver", "--port", "8080"]

# The default command (can be overridden)
CMD ["--port", "8080"]