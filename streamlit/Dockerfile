FROM python:latest

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    fonts-roboto fonts-inconsolata \
    && rm -rf /var/lib/apt/lists/*

COPY ./streamlit/requirements.txt ./requirements.txt
# Install Streamlit
RUN pip install --no-cache-dir -r requirements.txt 

COPY ./streamlit/app ./
# Expose the Streamlit port
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
#ENTRYPOINT ["python3", "-m", "http.server", "8501"]