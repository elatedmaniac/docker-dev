FROM ollama/ollama:latest

ARG MODEL
ENV MODEL=${MODEL}

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY /embeddings/Modelfile /Modelfile

RUN sed -i 's/${MODEL}/'"$MODEL"'/' /Modelfile

COPY /scripts/entrypoint-ollama.sh /root/entrypoint.sh

# Make sure the script is executable
RUN chmod +x ~/entrypoint.sh

# Expose the Ollama port
EXPOSE 11434

# Set the entrypoint to our custom script
ENTRYPOINT ["/root/entrypoint.sh"]