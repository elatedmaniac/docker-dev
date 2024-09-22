# Use the official Neo4j image
FROM neo4j:latest

# Set build arguments
ARG NEO4J_AUTH

# Set environment variables
ENV NEO4J_AUTH=${NEO4J_AUTH}

COPY ./certificates /var/lib/neo4j/certificates

COPY neo4j.conf /var/lib/neo4j/conf/neo4j.conf

# Expose necessary ports
EXPOSE 7474 7473 7687

RUN chmod 644 -R /var/lib/neo4j/certificates

