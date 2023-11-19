import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config
from service import Service
from notifier import notifier

class Checker:
    def __init__(self, services: list[Service]):
        self.services = services

    def check_services(self):
        while True:
            current_time = time.time()
            for service in self.services:
                if current_time - service.last_checked >= service.check_interval:
                    service.check_status()
                    service.last_checked = current_time
                    service.status_summary()
                    self.alert_if_needed(service)
                    
            time.sleep(1)

    def alert_if_needed(self, service: Service):
        if service.failed_checks > 0 and (service.total_checks % service.alert_period == 0):
            if not notifier:
                return
            
            subject = f"Status Alert: {service.name} - {service.host}:{service.port}"
            message = f"{service.name} at {service.host}:{service.port} is down. "\
                      f"Uptime: {service.calculate_uptime()}%\n"\
                      f"Total Checks: {service.total_checks}\n"\
                      f"Failed Checks: {service.failed_checks}\n"\
                      f"Failed Timestamps: {', '.join(service.failed_timestamps)}"
            
            notifier.send_email(config.recipient_email, subject, message)
            
            
if __name__ == "__main__":
    from yaml_reader import YamlReader
    yaml_reader = YamlReader(config.services_yaml)
    
    checker = Checker(yaml_reader.services)
    checker.check_services()