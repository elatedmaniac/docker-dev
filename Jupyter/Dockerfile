# Use a specific CUDA version to avoid unnecessary components
FROM nvidia/cuda:12.5.0-base-ubuntu22.04

# Set environment variables
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /usr/local/bin:$PATH
ENV TINI_VERSION v0.6.0
# Install Python and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    python3-venv \
    wget \
    git \
    sudo \
    openssl \
    tini \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash jupyter


# Create necessary directories
RUN mkdir -p /home/jupyter/.jupyter/ssl /notebooks /home/jupyter/.jupyter/lab/user-settings/@jupyterlab/apputils-extension

# Create a virtual environment and change ownership
RUN python3 -m venv /opt/venv && chown -R jupyter:jupyter /opt/venv

# Set environment variable to use venv
ENV PATH="/opt/venv/bin:$PATH"

# Set up Jupyter
WORKDIR /home/jupyter

# Change ownership of Jupyter directories
RUN chown -R jupyter:jupyter /home/jupyter/.jupyter /notebooks

# Copy Jupyter configuration and certificates
COPY --chown=jupyter:jupyter Jupyter/config/jupyter_application_config.py /home/jupyter/.jupyter/
COPY --chown=jupyter:jupyter Jupyter/certs /home/jupyter/.jupyter/ssl
COPY --chown=jupyter:jupyter scripts/entrypoint-anaconda.sh /home/jupyter/
COPY --chown=jupyter:jupyter Jupyter/overrides.json /opt/venv/share/jupyter/lab/settings/overrides.json

RUN chown -R jupyter:jupyter /opt/venv
# Ensure jupyter user has write access to necessary directories
RUN chmod 700 /home/jupyter/.jupyter && \
    chmod 600 /home/jupyter/.jupyter/*

# Switch to the jupyter user
USER jupyter

# Copy requirements.txt
COPY --chown=jupyter:jupyter Jupyter/requirements.txt /home/jupyter/

# Install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN jt -t chesterish -f ubuntu -fs 16 -cellw 80%

# Set working directory
WORKDIR /notebooks

# Expose port for Jupyter Notebook
EXPOSE 8888

ENTRYPOINT ["tini","--", "/home/jupyter/entrypoint-anaconda.sh"]
# Set the entrypoint to the script
