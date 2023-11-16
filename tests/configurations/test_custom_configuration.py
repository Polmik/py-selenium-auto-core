import pytest

from py_selenium_auto_core.applications.startup import ServiceProvider, Startup
from py_selenium_auto_core.utilities.json_settings_file import JsonSettingsFile


class FakeSettingsFile(JsonSettingsFile):
    def __init__(self):
        super().__init__({})


class TestCustomConfiguration:
    service_provider: ServiceProvider = None
    settings_file: FakeSettingsFile = FakeSettingsFile()

    def setup_method(self, method=None):
        def _predicate(service):
            raise NotImplementedError

        self.service_provider = Startup.configure_services(
            _predicate,
            self.settings_file,
        )

    @pytest.mark.skip(reason="Incorrect working with custom settings")
    def test_get_retry_config(self):
        retry_config = self.service_provider.retry_configuration()
        timeout_config = self.service_provider.timeout_configuration()
        logger_config = self.service_provider.logger_configuration()
        assert retry_config.polling_interval == 1, "Retry config should be received from custom setting file"
        assert timeout_config.polling_interval == 1, "Timeout config should be received from custom setting file"
        assert logger_config.language == "en", "Logger config should be received from custom setting file"
