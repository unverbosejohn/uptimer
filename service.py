import requests
import time

import config


class Service:
    def __init__(self, name: str, host: str, port: int, 
                 expected_response=200, check_interval=300, uptime_threshold=99.9, max_response_times=100):
        self.name = name
        self.host = host
        self.port = port
        self.expected_response = expected_response
        self.check_interval = check_interval
        self.uptime_threshold = uptime_threshold
        self.last_checked = 0
        self.total_checks = 0
        self.failed_checks = 0
        self.avg_response_time = 0.0
        self.uptime = 0.0
        self.failed_timestamps = []
        self.max_response_times = max_response_times
        self.response_times = []
        self.protocol = None
        self.status = "Online"

    def check_status(self):
        """
        _summary_: Checks the status of the service, sets instance attributes
        """
        if self.protocol is None:
            self.protocol = self.check_protocol(host=self.host, port=self.port)
        
        if self.protocol:
            self.check_service()
        
    def check_service(self):
        """
        _summary_: Checks the status of the service, sets instance attributes
        """
        self.total_checks += 1

        try:
            url = f"{self.protocol}://{self.host}:{self.port}"
            start_time = time.time()
            response = requests.get(url, timeout=config.default_timeout)
            end_time = time.time()

            response_time_ms = (end_time - start_time) * 1000
            self.response_times.append(response_time_ms)

            if len(self.response_times) > self.max_response_times:
                self.response_times.pop(0)

            if response.status_code != self.expected_response:
                self.log_failed_check()
            
            else:
                self.log_success_check()
                              
        except Exception as e:
            self.log_failed_check()
            
    def log_failed_check(self):
        self.failed_checks += 1
        self.failed_timestamps.append(time.strftime("%Y-%m-%d %H:%M:%S"))
        self.protocol = None
        self.status = "Offline"
        
    def log_success_check(self):
        self.status = "Online"

    def calculate_uptime(self) -> float:
        """
        Calculates the uptime of the service

        :return _type_: Percentage of uptime
        """
        if self.total_checks == 0:
            return 100.0
        else:
            uptime = ((self.total_checks - self.failed_checks) / self.total_checks) * 100
            return round(uptime, 2)

    def average_response_time(self) -> float:
        """
        _summary_: Calculates the average response time of the service

        :return _type_: Float representing the average response time
        """
        if self.response_times:
            return round(sum(self.response_times) / len(self.response_times), 2)
        else:
            return 0.0
        
    def as_dict(self) -> dict:
        """
        _summary_: Returns a dictionary containing the class attributes

        :return _type_: Dictionary representation of the instance
        """
        return {attr: getattr(self, attr) for attr in vars(self) if not callable(getattr(self, attr)) and not attr.startswith("__")}


    def status_summary(self) -> dict:
        """
        Returns a dictionary containing the status summary of the service

        :return _type_: Class object as a dictionary
        """
        self.uptime = self.calculate_uptime()
        self.avg_response_time = self.average_response_time()
            
        return self.as_dict()
    
    @staticmethod
    def check_protocol(host: str, port: int) -> str | None:
        """
        Attempts to determine the protocol (HTTP or HTTPS) of a service

        :param _type_ host: Hostname or IP address of the service
        :param _type_ port: Port number of the service
        :return _type_: String containing the protocol (http or https)
        """
        if port == 443:
            return 'https'
        elif port == 80:
            return 'http'
        
        https_url = f"https://{host}:{port}"
        try:
            response = requests.get(https_url, timeout=5)
            if response.status_code == 200:
                return 'https'
        
        except requests.exceptions.RequestException as e:
            pass

        http_url = f"http://{host}:{port}"
        try:
            response = requests.get(http_url, timeout=5)
            if response.status_code == 200:
                return 'http'
            
        except requests.exceptions.RequestException as e:
            return None


        return None

if __name__ == '__main__':
    service = Service(name='Test Service', host='127.0.0.1', port=5000, expected_response=200)
    print(service.check_protocol(host='127.0.0.1', port=5000))
    service.check_status()
    print(service.status_summary())