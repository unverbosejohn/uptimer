import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import app.config as config
from app.service import Service
from app.notifier import notifier
from app.database import Database
from app.logger import logger


class Checker:
    def __init__(self, services: list[Service]):
        self.services = services
        self.db = Database(config.db_file, 'app/services.sql')
        
    def check_services(self):
        while True:
            current_time = time.time()
            for service in self.services:
                logger.debug(f"[CHECKER][check_services] Checking {service.name} at {service.host}:{service.port}")
                if current_time - service.last_checked >= service.check_interval:
                    service.check_status()
                    service.last_checked = current_time
                    service.status_summary()
                    self.alert_and_log(service)
                    
            time.sleep(1)

    def alert_and_log(self, service: Service):
        # if service.failed_checks > 0 and (service.total_checks % service.alert_period == 0):
        if service.consecutive_failed_checks >= service.alert_period:
            logger.info(f"[CHECKER][alert_and_log][DOWN] {service.name} (Total {service.failed_checks} over {service.alert_period}) | {service.host}:{service.port}")
            service.log_failed_check()
            
            if not notifier:
                return
            
            subject = f"Status Alert: {service.name} - {service.host}:{service.port}"
            message = f"{service.name} at {service.host}:{service.port} is down. "\
                      f"Uptime: {service.calculate_uptime()}%\n"\
                      f"Total Checks: {service.total_checks}\n"\
                      f"Failed Checks: {service.failed_checks}\n"\
                      f"Failed Timestamps: {', '.join(service.failed_timestamps)}"
            
            logger.debug(f'[CHECKER][alert_and_log][NOTIFY] Sending email alert to {config.recipients_list}')
            for recipient in config.recipients_list:
                notifier.send_email(recipient, subject, message)
                time.sleep(1)
            
        else:
            logger.debug(f'[CHECKER][alert_and_log][UP] {service.name} | {service.host}:{service.port}')
            service.log_success_check()
        
    def close(self):
        self.db.close()
            
if __name__ == "__main__":
    from yaml_reader import YamlReader
    yaml_reader = YamlReader(config.services_yaml)
    
    checker = Checker(yaml_reader.services)
    checker.check_services()