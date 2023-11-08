from __future__ import annotations

import abc

from py_selenium_auto_core.utilities.json_settings_file import JsonSettingsFile


class BaseConfiguration(abc.ABC):
    def __init__(self, settings: dict | JsonSettingsFile, node_name: str):
        """Instantiates class using JsonSettingsFile or dict with general settings

        Args:
            settings: Settings file
            node_name: Key for getting information from Json
        """
        node: dict = self._dict_to_json_settings(settings).get(node_name)
        self._node: JsonSettingsFile = JsonSettingsFile(node)

    @classmethod
    def _dict_to_json_settings(cls, settings: dict | JsonSettingsFile) -> JsonSettingsFile:
        if isinstance(settings, dict):
            return JsonSettingsFile(settings)
        return settings
