import yaml
import os

ROOT_DIR = os.getcwd() + "/"

# Load configuration from config.yaml
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Basic
services_yaml = config.get('services_yaml')
db_file = config.get('db_file')
schema_file = config.get('schema_file')

# Logging
log_level = config['logging']['log_level']
abs_log_path = config['logging']['abs_log_path']

# Defaults
default_interval = config['defaults']['interval']
default_alert_period = config['defaults']['alert_period']
default_timeout = config['defaults']['timeout']

# Email settings
email_enabled = config['email']['enabled']
smtp_server = config['email']['smtp_server']
smtp_port = config['email']['smtp_port']
smtp_username = config['email']['smtp_username']
smtp_password = config['email']['smtp_password']
sender_email = config['email']['sender_email']
recipients_list = config['email']['recipients_list']

port = config.get('port')
