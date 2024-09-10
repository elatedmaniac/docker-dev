#!/bin/bash
set -e

# Start Jupyter Notebook with the log file location set to the new directory
jt -t chesterish -fs 16
jupyter notebook --config=/home/jupyter/.jupyter/jupyter_application_config.py --no-browser --ip=0.0.0.0 --port=8888 --notebook-dir=/notebooks
