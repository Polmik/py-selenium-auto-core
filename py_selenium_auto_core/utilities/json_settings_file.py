from __future__ import annotations

import json
from typing import overload, Any, Optional

from py_selenium_auto_core.utilities.environment_configuration import (
    EnvironmentConfiguration,
)
from py_selenium_auto_core.utilities.file_reader import FileReader


class JsonSettingsFile:
    """Class provides methods to get info from JSON files"""

    @overload
    def __init__(self, setting_json: dict):
        ...

    @overload
    def __init__(self, setting_name: str):
        ...

    @overload
    def __init__(self, setting_name: str, root_path: str):
        ...

    def __init__(self, setting_name: str | dict = None, root_path: str = None):
        """JsonSettingsFile constructor

        Args:
            setting_name (str|dict): Name of resource file or dictionary
            root_path: Root path which resource belongs to
        """
        if setting_name is None:
            raise ValueError("SettingName[str | dict] couldn't be None")
        if isinstance(setting_name, dict):
            self.setting_json: dict = setting_name
        else:
            self.setting_json: dict = json.loads(FileReader.get_resource_file(setting_name, root_path))

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Gets value from JSON

        Note that the value can be overriden via Environment variable with the same name
            (e.g. for json path "timeout_script" you can set environment variable "timeout_script")

        Args:
            key: Json key
            default: The default value to be set if the value is missing by key

        Returns:
            Value from Json
        """
        env_var = self._get_environment_value(key)
        if env_var is None:
            return self.setting_json.get(key, default)
        return env_var

    def get_as_int(self, key: str, default: Optional[Any] = None) -> int:
        return int(self.get(key, default))

    def get_as_bool(self, key: str, default: Optional[Any] = None) -> bool:
        return bool(self.get(key, default))

    def get_as_float(self, key: str, default: Optional[Any] = None) -> float:
        return float(self.get(key, default))

    @staticmethod
    def _get_environment_value(key: str) -> Any:
        return EnvironmentConfiguration.get_variable(key)
