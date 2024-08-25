#!/bin/bash

# Start ollama serve in the background
ollama serve &

# Wait for ollama serve to be ready
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    echo "Waiting for ollama serve to be ready..."
    sleep 1
done

ollama create $MODEL -f /Modelfile
# Run ollama run phi3:medium
ollama run $MODEL &

# Keep the container running
tail -f /dev/null