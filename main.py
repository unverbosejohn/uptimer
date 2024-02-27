import threading
import os
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime

import app.config as config
from app.checker import Checker
from app.yaml_reader import YamlReader
from app.helpers import hr_time
from app.logger import logger

# Load the services from the YAML file
services_to_monitor = YamlReader(config.services_yaml).services

app = Flask(__name__, static_url_path='/app/static')
Bootstrap(app)

checker = Checker(services_to_monitor)

service_start_time = datetime.utcnow()
logger.info(f'Service started at {service_start_time}')
# print(service_start_time)

def get_service_summaries():
    summaries = []
    for service in services_to_monitor:
        summaries.append(service.status_summary())
    return summaries

@app.route('/')
def dashboard():
    service_summaries = get_service_summaries()
    return render_template('dashboard.html', 
                           service_summaries=service_summaries, 
                           service_start_time=service_start_time,
                           hr_time=hr_time)

@app.route('/update-cards')
def update_cards():
    service_summaries = get_service_summaries()
    return render_template('cards_partial.html', 
                           service_summaries=service_summaries, 
                           hr_time=hr_time,
                           len=len)


def file_exists(path: str) -> bool:
    """Checks if the given path is valid

    :param path: absolute or relative path
    :return: True if the path exists, False otherwise
    """
    if os.path.exists(path):
        return True
    else:
        return False


if __name__ == '__main__':    
    checker_thread = threading.Thread(target=checker.check_services)
    checker_thread.start()
    app.run(host='0.0.0.0', port=config.port, debug=True)
