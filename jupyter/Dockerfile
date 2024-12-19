# Use a specific CUDA version to avoid unnecessary components
FROM nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH=/usr/local/bin:$PATH
ENV TINI_VERSION=v0.6.0

ARG CERTIFICATE_OU
ENV CERTIFICATE_OU=${CERTIFICATE_OU}

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.12 \
    python3-pip \
    python3-venv \
    wget \
    git \
    tini \
    sudo \
    openssl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Step 8: Create necessary directories including ssl
RUN useradd -m -s /bin/bash jupyter && \
    mkdir -p /home/jupyter/.jupyter/custom/fonts && \
    mkdir -p /home/jupyter/.jupyter/lab/user-settings/@jupyterlab/apputils-extension && \
    mkdir -p /notebooks && \
    mkdir -p /home/jupyter/.jupyter/ssl  # Added ssl directory

RUN chown -R jupyter:jupyter /home/jupyter && \
    chmod -R 755 /home/jupyter/.jupyter && \
    chown -R jupyter:jupyter /notebooks


# Create a virtual environment and change ownership
RUN python3 -m venv /opt/venv && \
    chown -R jupyter:jupyter /opt/venv

COPY --chown=jupyter:jupyter scripts/entrypoint-anaconda.sh /home/jupyter/entrypoint-anaconda.sh

RUN chmod +x /home/jupyter/entrypoint-anaconda.sh
# Install Python packages as jupyter user
USER jupyter
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements.txt
COPY --chown=jupyter:jupyter jupyter/requirements.txt /home/jupyter/requirements.txt
# Install Python packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /home/jupyter/requirements.txt

# Set up Jupyter
WORKDIR /home/jupyter

# Change ownership of Jupyter directories
RUN chown -R jupyter:jupyter /home/jupyter /notebooks /home/jupyter/.jupyter/ssl

# Copy Jupyter configuration and certificates
COPY --chown=jupyter:jupyter jupyter/config/jupyter_application_config.py /home/jupyter/.jupyter/jupyter_application_config.py
COPY --chown=jupyter:jupyter jupyter/overrides.json /opt/venv/share/jupyter/lab/settings/overrides.json

RUN chown -R jupyter:jupyter /opt/venv && mkdir -p /home/jupyter/.jupyter/ssl && \
    cd /home/jupyter/.jupyter/ssl && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout jupyter.key \
    -out jupyter.crt \
    -subj "/C=GR/ST=Attica/L=Athens/O=Olympus/OU=Gods/CN=jupyter.${CERTIFICATE_OU}" && \
    chmod 644 /home/jupyter/.jupyter/ssl/jupyter.crt && \
    chmod 644 /home/jupyter/.jupyter/ssl/jupyter.key && \
    chown -R jupyter:jupyter /home/jupyter/.jupyter/ssl

# Expose port for Jupyter Notebook
EXPOSE 8888

ENTRYPOINT ["tini","--", "/home/jupyter/entrypoint-anaconda.sh"]
# Set the entrypoint to the script
