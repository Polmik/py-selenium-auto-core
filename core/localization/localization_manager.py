import json
import os
from typing import Optional

from core import ROOT_PATH_CORE
from core.configurations.logger_configuration import LoggerConfiguration
from core.logging.logger import Logger
from core.utilities.file_reader import FileReader


class LocalizationManager:
    _lang_resource = "localization\\{0}.json"
    logger = None

    def __init__(self, logger_configuration: LoggerConfiguration, logger: Logger, root_path: Optional[str] = None):
        language = logger_configuration.language
        self.__localization_file = self.__get_localization_file(language, root_path or ROOT_PATH_CORE)
        self.__core_localization_file = self.__get_localization_file(language, ROOT_PATH_CORE)
        self.logger = logger

    def get_localized_message(self, message_key: str, *args) -> str:
        local_to_use = self.__localization_file if message_key in self.__localization_file else self.__core_localization_file
        if message_key in local_to_use:
            return local_to_use.get(message_key).format(*args)
        self.logger.debug(f"Cannot find localized message by key '{message_key}'")
        return message_key

    def __get_localization_file(self, language: str, root_path: str) -> dict:
        resource_name = self._lang_resource.format(language)
        resource_path = FileReader.get_resource_file(resource_name, root_path)
        if not os.path.exists(resource_path):
            resource_path = os.path.join(ROOT_PATH_CORE, resource_name)
        with open(resource_path, "r") as file:
            return json.loads(file.read())
