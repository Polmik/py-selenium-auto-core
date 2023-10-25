from __future__ import annotations

from python_selenium_core.configurations.base_configurations import BaseConfiguration
from python_selenium_core.utilities.json_settings_file import JsonSettingsFile


class RetryConfiguration(BaseConfiguration):

    def __init__(self, settings: dict | JsonSettingsFile):
        super().__init__(settings, "retry")

    @property
    def number(self) -> int:
        return self._node.get_as_int("number")

    @property
    def polling_interval(self) -> float:
        return self._node.get_as_float("pollingInterval")
