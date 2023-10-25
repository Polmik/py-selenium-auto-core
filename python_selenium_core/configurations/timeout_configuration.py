from __future__ import annotations

from python_selenium_core.configurations.base_configurations import BaseConfiguration
from python_selenium_core.utilities.json_settings_file import JsonSettingsFile


class TimeoutConfiguration(BaseConfiguration):

    def __init__(self, settings: dict | JsonSettingsFile):
        super().__init__(settings, "timeouts")

    @property
    def implicit(self) -> float:
        return self._node.get_as_float("timeoutImplicit")

    @property
    def condition(self) -> float:
        return self._node.get_as_float("timeoutCondition")

    @property
    def polling_interval(self) -> float:
        return self._node.get_as_float("timeoutPollingInterval")

    @property
    def command(self) -> float:
        return self._node.get_as_float("timeout_command")
