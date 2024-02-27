import logging


class Logger:
    def __init__(self, level: str = None, output: str = None):
        self.level = level
        self.output = output
        self.setup_logging()
        # sys.stdout = sys.stderr = logging.getLogger().handlers[0].stream

    def setup_logging(self):
        if self.level == 'info':
            level = logging.INFO

        elif self.level == 'debug':
            level = logging.DEBUG

        elif self.level in ['warn', 'warning']:
            level = logging.WARNING

        elif self.level == 'error':
            level = logging.ERROR

        elif self.level == 'fatal':
            level = logging.FATAL

        else:
            level = logging.DEBUG

        if self.output:
            logging.basicConfig(level=level, filename=f'{self.output}',
                                format='%(asctime)s [%(levelname)s] %(message)s')

        else:
            logging.basicConfig(level=level, format='%(asctime)s [%(levelname)s] %(message)s')

    @staticmethod
    def log(level: str = 'debug', message: str = None):
        if level == 'debug':
            logging.debug(message)
        elif level == 'info':
            logging.info(message)
        elif level == 'warn' or level == 'warning':
            logging.warning(message)
        elif level == 'error':
            logging.error(message)
        elif level == '':
            logging.fatal(message)

    @staticmethod
    def info(message: str = None):
        logging.info(message)

    @staticmethod
    def debug(message: str = None):
        logging.debug(message)

    @staticmethod
    def warn(message: str = None):
        logging.warning(message)

    @staticmethod
    def warning(message: str = None):
        logging.warning(message)

    @staticmethod
    def error(message: str = None):
        logging.error(message)

    @staticmethod
    def fatal(self, message: str = None):
        logging.fatal(message)


if __name__ == '__main__':
    logger = Logger('debug', 'testing.log')
    logger.info('Test log')
