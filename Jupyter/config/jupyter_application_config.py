import os
from jupyter_server.auth import passwd

c = get_config()

# Set the IP address and port
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888

# Enable SSL/HTTPS
c.NotebookApp.certfile = '/home/jupyter/.jupyter/ssl/jupyter.crt'
c.NotebookApp.keyfile = '/home/jupyter/.jupyter/ssl/jupyter.key'

# Disable password requirement (for development only, enable for production)
c.NotebookApp.token = ''
c.NotebookApp.password = ''

# Allow requests from all origins (for development only, restrict for production)
c.NotebookApp.allow_origin = '*'

# Set the notebook directory
c.NotebookApp.notebook_dir = '/notebooks'

# Other configurations
c.NotebookApp.open_browser = False

# Set a password
password = os.environ.get('JUPYTER_PASSWORD', 'default_password')
c.ServerApp.password = passwd(password)


# Enable token authentication for additional security
c.ServerApp.token = 'e1b4829774c7f23038d75f0b0fd70c5f18d6daf62ac7bd85'  # Set this to a secure token if you want to use token authentication

# Allow root to run the notebook
c.ServerApp.allow_root = False
