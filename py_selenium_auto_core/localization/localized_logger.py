from py_selenium_auto_core.configurations.logger_configuration import (
    LoggerConfiguration,
)
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.logging.logger import Logger


class LocalizedLogger:
    def __init__(
        self,
        localization_manager: LocalizationManager,
        logger: Logger,
        logger_configuration: LoggerConfiguration,
    ):
        self.__localization_manager = localization_manager
        self.__logger = logger
        self.configuration = logger_configuration

    def info_element_action(self, element_type: str, element_name: str, message_key: str, *args):
        localized_message = self.__localization_manager.get_localized_message(message_key, *args)
        self.__logger.info(f"{element_type} '{element_name}' :: {localized_message}")

    def info(self, message_key: str, *args):
        localized_message = self.__localization_manager.get_localized_message(message_key, *args)
        self.__logger.info(localized_message)

    def debug(self, message_key: str, exception: Exception = None, *args):
        localized_message = self.__localization_manager.get_localized_message(message_key, *args)
        self.__logger.debug(localized_message, exc_info=exception)

    def warn(self, message_key: str, *args):
        localized_message = self.__localization_manager.get_localized_message(message_key, *args)
        self.__logger.warn(localized_message)

    def error(self, message_key: str, *args):
        localized_message = self.__localization_manager.get_localized_message(message_key, *args)
        self.__logger.error(localized_message)

    def fatal(self, message_key: str, exception: Exception = None, *args):
        localized_message = self.__localization_manager.get_localized_message(message_key, *args)
        self.__logger.fatal(localized_message, exc_info=exception)
