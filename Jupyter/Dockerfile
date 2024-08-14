# Use a specific CUDA version to avoid unnecessary components
FROM nvidia/cuda:12.5.0-base-ubuntu22.04

# Set environment variables
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /usr/local/bin:$PATH

# Install Python and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    python3-venv \
    wget \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash jupyter

# Create a virtual environment and change ownership
RUN python3 -m venv /opt/venv && chown -R jupyter:jupyter /opt/venv

# Set environment variable to use venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    jupyter \
    jupyterlab \
    torch \
    torchvision \
    torchaudio \
    transformers \
    neo4j \
    pandas

# Set up Jupyter
RUN mkdir -p /home/jupyter/.jupyter/ssl /notebooks
WORKDIR /home/jupyter

# Copy Jupyter configuration and certificates
COPY --chown=jupyter:jupyter /Jupyter/certs/* /home/jupyter/.jupyter/ssl/
COPY --chown=jupyter:jupyter /Jupyter/config/jupyter_application_config.py /home/jupyter/.jupyter/jupyter_notebook_config.py

# Ensure jupyter user has write access to necessary directories
RUN chmod 755 /home/jupyter/.jupyter

# Set working directory
WORKDIR /notebooks

# Switch to the jupyter user
USER jupyter
# Expose port for Jupyter Notebook
EXPOSE 8888

# Set the entrypoint to the script
CMD ["jupyter", "notebook", "--config=/home/jupyter/.jupyter/jupyter_notebook_config.py", "--no-browser", "--ip=0.0.0.0", "--port=8888", "--notebook-dir=/notebooks"]