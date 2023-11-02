import os

from tests.test_without_application import TestWithoutApplication


class TestConfiguration(TestWithoutApplication):

    def setup_method(self, method=None):
        os.environ["profile"] = "custom"
        super().setup_method()

    def teardown_method(self, method):
        os.environ["profile"] = ""

    def test_should_get_configuration_from_custom_profile(self):
        assert "ru" == self.service_provider.logger_configuration().language
