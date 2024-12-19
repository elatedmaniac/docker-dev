# Use the official Neo4j image
FROM neo4j:latest

# Set build arguments
ARG NEO4J_AUTH
ARG CERTIFICATE_OU
ENV CERTIFICATE_OU=${CERTIFICATE_OU}

RUN mkdir -p /var/lib/neo4j/certificates && openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /var/lib/neo4j/certificates/private.key \
    -out /var/lib/neo4j/certificates/public.crt \
    -subj "/C=GR/ST=Attica/L=Athens/O=Olympus/OU=Gods/CN=neo4j.${CERTIFICATE_OU}"

# Set environment variables
ENV NEO4J_AUTH=${NEO4J_AUTH}

COPY neo4j.conf /var/lib/neo4j/conf/neo4j.conf

# Expose necessary ports
EXPOSE 7474 7473 7687

RUN chmod 644 -R /var/lib/neo4j/certificates

