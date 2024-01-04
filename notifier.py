import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config

class Notifier:
    _instance = None

    def __new__(cls, smtp_server, smtp_port, smtp_username, smtp_password, sender_email):
        if cls._instance is None:
            cls._instance = super(Notifier, cls).__new__(cls)
            cls._instance.smtp_server = smtp_server
            cls._instance.smtp_port = smtp_port
            cls._instance.smtp_username = smtp_username
            cls._instance.smtp_password = smtp_password
            cls._instance.sender_email = sender_email
        return cls._instance

    def send_email(self, recipient_email, subject, message):
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)

            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            server.sendmail(self.sender_email, recipient_email, msg.as_string())

            server.quit()
        except Exception as e:
            print(f"Failed to send email: {e}")

if config.email_enabled:
    notifier = Notifier(config.smtp_server, config.smtp_port, config.smtp_username, config.smtp_password, config.sender_email)
else:
    notifier = None
    
    
if __name__ == '__main__':
    notifier = Notifier(config.smtp_server, config.smtp_port, config.smtp_username, config.smtp_password, config.sender_email)
    notifier.send_email('dev@email.com', 'Test', 'Test message')