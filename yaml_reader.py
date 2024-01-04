import yaml

import config
from service import Service
from database import Database

class YamlReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.services = self.read_services()

    def read_services(self):
        services = []
        try:
            with open(self.file_path, 'r') as yaml_file:
                data = yaml.safe_load(yaml_file)

                for service_data in data['services']:
                    name = service_data['name']
                    host = service_data['host']
                    port = service_data['port']
                    expected_response = service_data['expected_response']
                    expected_json_response = service_data.get('expected_json_response', None)
                    check_interval = service_data.get('check_interval', 300) 
                    alert_period = service_data.get('alert_period', 3600)
                    

                    service = Service(name=name, 
                                      host=host, 
                                      port=port, 
                                      expected_response=expected_response,
                                      expected_json_response=expected_json_response,
                                      db=Database(config.db_file, config.schema_file))
                    
                    service.check_interval = check_interval
                    service.alert_period = alert_period

                    services.append(service)

        except FileNotFoundError:
            print(f"File not found: {self.file_path}")
        except Exception as e:
            print(f"Error reading YAML file: {str(e)}")

        return services

if __name__ == "__main__":
    yaml_reader = YamlReader("services.yaml")
    services = yaml_reader.read_services()

    for service in services:
        print(service.status_summary())
