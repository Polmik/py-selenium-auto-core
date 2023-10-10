from typing import Callable

from core.applications.startup import ServiceProvider, Startup
from core.tests.applications.browser.browser_service import BrowserService


class TestWithBrowser:
    test_site: str = "http://the-internet.herokuapp.com"

    service_provider: ServiceProvider = None

    def setup_method(self, method):
        self.service_provider = CustomStartup.configure_services(lambda service: BrowserService.application())
        BrowserService.set_service_provider(self.service_provider)

    def teardown_method(self, method):
        if BrowserService.is_application_started():
            BrowserService.application().quit()


class CustomStartup(Startup):

    @staticmethod
    def configure_services(application_provider: Callable, settings: dict = None) -> ServiceProvider:
        service_provider = Startup.configure_services(application_provider, settings)
        return service_provider
