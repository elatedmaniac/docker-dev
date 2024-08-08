import os
from notebook.auth import passwd

c = get_config()

# Set the IP address and port
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888

# Set the paths to the SSL certificate and key
c.NotebookApp.certfile = '/certs/jupyter.crt'
c.NotebookApp.keyfile = '/certs/jupyter.key'

# Disable browser opening
c.NotebookApp.open_browser = False

# Set a password
password = os.getenv('JUPYTER_PASSWORD', 'default_password')
c.NotebookApp.password = passwd(password)
