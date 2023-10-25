from __future__ import annotations

from python_selenium_core.configurations.base_configurations import BaseConfiguration
from python_selenium_core.utilities.json_settings_file import JsonSettingsFile


class ElementCacheConfiguration(BaseConfiguration):

    def __init__(self, settings: dict | JsonSettingsFile):
        super().__init__(settings, "elementCache")

    @property
    def is_enabled(self) -> bool:
        return self._node.get_as_bool("elementCache")
