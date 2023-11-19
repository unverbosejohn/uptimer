import requests
import time


class Service:
    def __init__(self, name, host, port, expected_response, check_interval=300, uptime_threshold=99.9, max_response_times=100):
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
        self.status = "Online"

    def check_status(self):
        try:
            url = f"http://{self.host}:{self.port}"
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()

            response_time_ms = (end_time - start_time) * 1000
            print(response_time_ms)
            self.response_times.append(response_time_ms)

            if len(self.response_times) > self.max_response_times:
                self.response_times.pop(0)

            self.total_checks += 1

            if response.status_code != self.expected_response:
                self.failed_checks += 1
                self.failed_timestamps.append(time.strftime("%Y-%m-%d %H:%M:%S"))
                self.status = "Offline"
            
            else:
                self.status = "Online"
                
        except Exception as e:
            self.total_checks += 1
            self.failed_checks += 1
            self.failed_timestamps.append(time.strftime("%Y-%m-%d %H:%M:%S"))
            self.status = "Offline"

    def calculate_uptime(self):
        if self.total_checks == 0:
            return 100.0
        else:
            uptime = ((self.total_checks - self.failed_checks) / self.total_checks) * 100
            return round(uptime, 2)

    def average_response_time(self):
        if self.response_times:
            return round(sum(self.response_times) / len(self.response_times), 2)
        else:
            return 0.0
        
    def as_dict(self):
        return {attr: getattr(self, attr) for attr in vars(self) if not callable(getattr(self, attr)) and not attr.startswith("__")}


    def status_summary(self):
        self.uptime = self.calculate_uptime()
        self.avg_response_time = self.average_response_time()
            
        return self.as_dict()
