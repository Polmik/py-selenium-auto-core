import json
import os
from typing import Optional

from py_selenium_auto_core.configurations.logger_configuration import (
    LoggerConfiguration,
)
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper
from py_selenium_auto_core.utilities.file_reader import FileReader


class LocalizationManager:
    _lang_resource_dir = "localization"
    _lang_resource_file = "{0}.json"
    logger = None

    def __init__(
        self,
        logger_configuration: LoggerConfiguration,
        logger: Logger,
        root_path: Optional[str] = None,
    ):
        language = logger_configuration.language
        self.__localization_file = self.__get_localization_file(
            language,
            root_path or RootPathHelper.current_root_path(__file__),
        )
        self.__core_localization_file = self.__get_localization_file(
            language,
            RootPathHelper.current_root_path(__file__),
        )
        self.logger = logger

    def get_localized_message(self, message_key: str, *args) -> str:
        local_to_use = (
            self.__localization_file if message_key in self.__localization_file else self.__core_localization_file
        )
        if message_key in local_to_use:
            return local_to_use.get(message_key).format(*args)
        self.logger.debug(f"Cannot find localized message by key '{message_key}'")
        return message_key

    def __get_localization_file(self, language: str, root_path: str) -> dict:
        resource_name = os.path.join(self._lang_resource_dir, self._lang_resource_file.format(language))
        root_path_to_use = (
            root_path
            if FileReader.is_resource_file_exist(resource_name, root_path)
            else RootPathHelper.current_root_path(__file__)
        )
        return json.loads(FileReader.get_resource_file(resource_name, root_path_to_use))
