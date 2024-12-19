# Use the official Nginx image as a base
FROM nginx:latest

# Install OpenSSL for generating SSL certificates
RUN apt-get update && \
    apt-get install -y openssl && \
    rm -rf /var/lib/apt/lists/*

# Create directory for SSL certificates
RUN mkdir -p /etc/nginx/certificates

# Generate a self-signed SSL certificate for dev.elatedmaniac.io
RUN openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/nginx/certificates/dev.elatedmaniac.io.key \
    -out /etc/nginx/certificates/dev.elatedmaniac.io.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=Department/CN=dev.elatedmaniac.io"

# Copy custom Nginx configuration file
COPY /nginx/nginx.conf /etc/nginx/nginx.conf

# Optionally, expose ports if not already exposed in nginx.conf
EXPOSE 80 443
