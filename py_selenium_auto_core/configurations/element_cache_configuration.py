from __future__ import annotations

from py_selenium_auto_core.configurations.base_configurations import BaseConfiguration
from py_selenium_auto_core.utilities.json_settings_file import JsonSettingsFile


class ElementCacheConfiguration(BaseConfiguration):
    """Provides element's cache configuration"""

    def __init__(self, settings: dict | JsonSettingsFile):
        """Instantiates class using JsonSettingsFile or dict with general settings

        Args:
            settings: Settings file
        """
        super().__init__(settings, "elementCache")

    @property
    def is_enabled(self) -> bool:
        return self._node.get_as_bool("elementCache")
