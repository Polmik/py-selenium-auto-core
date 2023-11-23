from py_selenium_auto_core.applications.startup import ServiceProvider, Startup


class TestWithoutApplication:
    service_provider: ServiceProvider

    def setup_method(self, method=None):
        def _predicate():
            raise NotImplementedError("Application should not be required")

        self.service_provider = Startup.configure_services(_predicate)
