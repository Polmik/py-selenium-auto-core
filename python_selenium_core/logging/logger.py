import logging
import os

from pathlib import Path


class Logger:
    __log = None

    @classmethod
    def _instance(cls):
        if cls.__log is None:
            cls.__log = logging.getLogger()
            cls.__configure_logger()
        return cls.__log

    @classmethod
    def info(cls, msg):
        cls._instance().info(msg)

    @classmethod
    def debug(cls, msg, exc_info: Exception = None):
        cls._instance().debug(msg, exc_info=exc_info)

    @classmethod
    def warn(cls, msg):
        cls._instance().warn(msg)

    @classmethod
    def error(cls, msg):
        cls._instance().error(msg)

    @classmethod
    def fatal(cls, msg, exc_info: Exception = None):
        cls._instance().fatal(msg, exc_info=exc_info)

    @classmethod
    def __configure_logger(cls):
        log_path = os.path.join(Path(__file__).parent.parent.parent, "Log\\log.log")

        if not os.path.exists(os.path.dirname(log_path)):
            os.mkdir(os.path.dirname(log_path))

        cls.__log.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-5.5s]  %(message)s")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        logging.getLogger().addHandler(stream_handler)
        logging.getLogger().addHandler(file_handler)
