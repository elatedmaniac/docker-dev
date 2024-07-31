#!/bin/bash
set -e

# Create a log directory with the container ID
CONTAINER_ID=$(basename $(cat /proc/1/cpuset))
LOG_DIR=/workspace/logs/$CONTAINER_ID
mkdir -p $LOG_DIR

# Start Jupyter Notebook with the log file location set to the new directory
exec jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --logfile=$LOG_DIR/jupyter.log