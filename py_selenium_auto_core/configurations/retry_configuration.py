from __future__ import annotations

from py_selenium_auto_core.configurations.base_configurations import BaseConfiguration
from py_selenium_auto_core.utilities.json_settings_file import JsonSettingsFile


class RetryConfiguration(BaseConfiguration):
    """Provides retry configuration"""

    def __init__(self, settings: dict | JsonSettingsFile):
        """Instantiates class using JsonSettingsFile or dict with general settings

        Args:
            settings: Settings file
        """
        super().__init__(settings, "retry")

    @property
    def number(self) -> int:
        return self._node.get_as_int("number")

    @property
    def polling_interval(self) -> float:
        return self._node.get_as_float("pollingInterval")
