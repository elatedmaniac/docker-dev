# Use the official NVIDIA CUDA image as a base
FROM nvidia/cuda:12.5.0-devel-ubuntu22.04 AS base

# Set environment variables
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

# Install basic utilities
RUN apt-get update --fix-missing && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    curl \
    git \
    net-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && /bin/bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda \
    && rm Miniconda3-latest-Linux-x86_64.sh

# Create a working directory
WORKDIR /workspace

# Create a conda environment and install necessary packages
RUN conda install -y python=3.11 \
    && conda install -y jupyter \
    && pip install --no-cache-dir \
    torch \
    torchvision \
    torchaudio \
    transformers \
    jupyterlab \
    neo4j \
    pandas \
    seaborn \
    && apt-get update -y && apt upgrade -y

FROM base 

# Create a working directory
WORKDIR /scripts

# Copy entrypoint script
COPY /scripts/entrypoint-logs.sh /scripts/entrypoint.sh
RUN chmod +x /scripts/entrypoint.sh

# Expose port for Jupyter Notebook
EXPOSE 8888

# Set the entrypoint to the script
ENTRYPOINT ["/scripts/entrypoint.sh"]

