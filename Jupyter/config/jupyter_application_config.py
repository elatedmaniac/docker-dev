import os
from jupyter_server.auth import passwd

c = get_config()

# Set the IP address and port
c.ServerApp.ip = '0.0.0.0'  # Allows connections from any IP
c.ServerApp.port = 8888
c.ServerApp.allow_origin = '*'  # Allows connections from any origin
c.ServerApp.open_browser = False

# Set the paths to the SSL certificate and key
# Comment these out if you're not using HTTPS directly on Jupyter
c.ServerApp.certfile = '/root/.jupyter/ssl/jupyter.crt'
c.ServerApp.keyfile = '/root/.jupyter/ssl/jupyter.key'

# Set a password
password = os.environ.get('JUPYTER_PASSWORD', 'default_password')
c.ServerApp.password = passwd(password)

# Set the notebook directory
c.ServerApp.notebook_dir = '/notebooks'

# Enable token authentication for additional security
c.ServerApp.token = 'e1b4829774c7f23038d75f0b0fd70c5f18d6daf62ac7bd85'  # Set this to a secure token if you want to use token authentication

# Allow root to run the notebook
c.ServerApp.allow_root = True
