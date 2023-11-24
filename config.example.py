

services_yaml = 'services.yaml'

# Default interval --Will be used if no other interval is specified in the YAML file
default_interval = 120  # 2 minutes

# Default alert period --Will be used if no other alert period is specified in the YAML file
default_alert_period = 300  # 5 minutes

# Default timeout
default_timeout = 10  # seconds

# Email settings
email_enabled = False
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_username = 'your_username'
smtp_password = 'your_password'
sender_email = ''

# API port
port = 5000