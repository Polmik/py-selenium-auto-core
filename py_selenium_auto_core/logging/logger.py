import logging
import os

from pathlib import Path
from typing import Optional

from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper


class Logger:
    """This class is using for a creating extended log. It implements a Singleton pattern"""

    __log = None

    @classmethod
    def _instance(cls):
        """Gets Logger instance"""
        if cls.__log is None:
            cls.__log = logging.getLogger()
            cls.__configure_logger()
        return cls.__log

    @classmethod
    def info(cls, msg, *args):
        """Log info message

        Args:
            msg: Message
        """
        cls._instance().info(msg, *args)

    @classmethod
    def debug(cls, msg, exc_info: Optional[Exception] = None):
        """Log debug message and optional exception

        Args:
            msg: Message
            exc_info: Exception
        """
        cls._instance().debug(msg, exc_info=exc_info)

    @classmethod
    def warn(cls, msg):
        """Log warning message

        Args:
            msg: Message
        """
        cls._instance().warning(msg)

    @classmethod
    def error(cls, msg):
        """Log error message

        Args:
            msg: Message
        """
        cls._instance().error(msg)

    @classmethod
    def fatal(cls, msg, exc_info: Optional[Exception] = None):
        """Log fatal message and exception

        Args:
            msg: Message
            exc_info: Exception
        """
        cls._instance().fatal(msg, exc_info=exc_info)

    @classmethod
    def __configure_logger(cls):
        """Method to configure logging"""
        log_path = os.path.join(Path(RootPathHelper.calling_root_path()).parent, "Log", "log.log")

        if not os.path.exists(os.path.dirname(log_path)):
            os.mkdir(os.path.dirname(log_path))

        cls.__log.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-5.5s]  %(message)s")

        # Stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)

        # File handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)

        logging.getLogger().addHandler(stream_handler)
        logging.getLogger().addHandler(file_handler)
