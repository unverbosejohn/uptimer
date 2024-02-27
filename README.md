# Service Status Dashboard

<img src="https://github.com/unverbosejohn/uptimer/blob/main/static/images/dashboard.jpg?raw=true" width="800" alt="Uptimer dashboard">

## Overview
This Service Status Dashboard is a web application designed to display the status of various services in real-time. It provides an easy-to-understand visual representation of the operational status of each service.

## Features
- **Real-Time Status Updates**: Displays the current status (Online/Offline) of services.
- **Dynamic Content Refresh**: Uses AJAX to partially reload card information without refreshing the entire page.
- **Mail/Slack/Teams Notifications** (future): Notify contacts if a service remains
offline after a set period.

## Setup and Installation

### Configuring Services
1. **Services Configuration**: 
   - Define your services in `services.yaml`.

2. **Setting up Configuration File**:
   - Rename `config.example.yaml` to `config.yaml`.
   - Edit `config.yaml` to suit your environment and preferences, such as default values, smpt server details, Slack/Teams tokens, etc.

### Running the Dashboard
- After configuring the services and settings, run main.py script to start the dashboard.
- Access the dashboard through your preferred web browser to view the status of the services.

## Usage
- The dashboard is intended for system administrators or users who need to monitor the status of various services.
- Each card on the dashboard represents a service, showing its current status, uptime, response time, and other relevant details.

**Production ready**:
   - Create a vitrtual environment from the project's root directory:
   ```
   mkdir venv
   python3 -m venv venv
   source venv/bin/activate
   ```
   - Install requirements
   ```
   pip install -r requirements.txt
   ```
   - Install gunicorn
   ```
   sudo apt install gunicorn
   pip install gunicorn
   ```
   - Run the service
   ```
   gunicorn -w 4 -b 0.0.0.0:5000 main:app
   ```
   - Access your dashboard at http://127.0.0.1:5000

**Building and running as a docker container**
- From the project root: docker build -t uptimer:latest .
- Make sure to correctly map services.yaml and config.yaml
- /usr/bin/docker run --rm --name uptimer_service \
   -p 5001:5001 \
   -v /root/uptimer/config.yaml:/usr/src/app/config.yaml \
   -v /root/uptimer/services.yaml:/usr/src/app/services.yaml \
   --log-driver=syslog uptimer:latest

## Technical Details
- The dashboard frontend is built using HTML, CSS, and JavaScript.
- AJAX is used for dynamically updating the service cards, enhancing the user experience by avoiding full page reloads.

## Contributing
- Contributions to the dashboard are welcome. Please refer to the contribution guidelines for more information.

## License
- Standard MIT license

## Author
John Geroitos

---

**Note**: Feel free to alter or improve any aspect of the service
