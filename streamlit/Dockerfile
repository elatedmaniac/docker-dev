FROM python:latest

# Install Streamlit
RUN pip install streamlit

# Copy the Streamlit app
COPY ./app /app

# Set the working directory
WORKDIR /app

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
