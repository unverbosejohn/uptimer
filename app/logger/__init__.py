from app.logger._logger import Logger
from app.config import log_level, abs_log_path

if abs_log_path:
    logger = Logger(level=log_level, output=abs_log_path)
    logger.info(f'Logger initialized with level {logger.level} and file {abs_log_path}')
else:
    logger = Logger(level=log_level)
    logger.info(f'Logger initialized with level {logger.level} and directs to syslog')
