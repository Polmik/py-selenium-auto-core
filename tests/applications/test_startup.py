import os

from py_selenium_auto_core.applications.startup import Startup


class TestStartup:
    def setup_method(self):
        os.environ["profile"] = "special"

    def teardown_method(self):
        os.environ["profile"] = ""

    def test_get_configuration_from_custom_profile(self):
        def _predicate(service):
            raise ValueError("Application should not be required")

        startup = Startup()
        service_provider = startup.configure_services(_predicate, startup.get_settings())
        assert service_provider.logger_configuration().language == "special"
