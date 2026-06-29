import logging
import sys


class LogService:
    def __init__(self, log_file: str = "app.log"):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.propagate = False

        print("LOGGER READY")

    def info(self, message: str, **kwargs):
        self.logger.info(f"{message} | {kwargs}")

    def error(self, message: str, **kwargs):
        self.logger.error(f"{message} | {kwargs}")


log_service = LogService()
