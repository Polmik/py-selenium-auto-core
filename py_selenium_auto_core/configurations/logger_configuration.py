from __future__ import annotations

from py_selenium_auto_core.configurations.base_configurations import BaseConfiguration
from py_selenium_auto_core.utilities.json_settings_file import JsonSettingsFile


class LoggerConfiguration(BaseConfiguration):
    """Provides logger configuration"""

    __default_language = "en"

    def __init__(self, settings: dict | JsonSettingsFile):
        """Instantiates class using JsonSettingsFile or dict with general settings

        Args:
            settings: Settings file
        """
        super().__init__(settings, "logger")

    @property
    def language(self) -> str:
        return self._node.get("language", "en")

    @property
    def log_page_source(self) -> bool:
        return self._node.get_as_bool("logPageSource", True)
