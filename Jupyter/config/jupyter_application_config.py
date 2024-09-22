import os
from jupyter_server.auth import passwd

c = get_config()

# Set the IP address and port
c.ServerApp.ip = '0.0.0.0'
c.ServerApp.port = 8888

# Enable SSL/HTTPS
c.ServerApp.certfile = '/home/jupyter/.jupyter/ssl/jupyter.crt'
c.ServerApp.keyfile = '/home/jupyter/.jupyter/ssl/jupyter.key'

# Disable password requirement (for development only, enable for production)
c.NotebookApp.token = ''
c.NotebookApp.password = ''

# Allow requests from all origins (for development only, restrict for production)
c.ServerApp.allow_origin = '*'

# Set the notebook directory
c.ServerApp.notebook_dir = '/notebooks'

# Other configurations
c.NotebookApp.open_browser = False

# Set a password
password = os.environ.get('JUPYTER_PASSWORD', 'default_password')
c.ServerApp.password = passwd(password)


# Enable token authentication for additional security
c.ServerApp.token = ''  # Set this to a secure token if you want to use token authentication

# Allow root to run the notebook
c.ServerApp.allow_root = False
