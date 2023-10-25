from __future__ import annotations

import abc

from python_selenium_core.utilities.json_settings_file import JsonSettingsFile


class BaseConfiguration(abc.ABC):

    def __init__(self, settings: dict | JsonSettingsFile, node_name: str):
        node = self._dict_to_json_settings(settings).get(node_name)
        self._node: JsonSettingsFile = JsonSettingsFile(node)

    @classmethod
    def _dict_to_json_settings(cls, settings: dict | JsonSettingsFile) -> JsonSettingsFile:
        if isinstance(settings, dict):
            return JsonSettingsFile(settings)
        return settings
