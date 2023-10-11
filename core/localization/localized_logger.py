from core.configurations.logger_configuration import LoggerConfiguration
from core.localization.localization_manager import LocalizationManager
from core.logging.logger import Logger


class LocalizedLogger:

    def __init__(
            self,
            localization_manager: LocalizationManager,
            logger: Logger,
            logger_configuration: LoggerConfiguration
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

    def debug(self, message_key: str, *args):
        localized_message = self.__localization_manager.get_localized_message(message_key, *args)
        self.__logger.debug(localized_message)
