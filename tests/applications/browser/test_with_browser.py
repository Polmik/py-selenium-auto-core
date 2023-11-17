from typing import Callable, Optional

from selenium.common import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from py_selenium_auto_core.applications.startup import ServiceProvider, Startup
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.json_settings_file import JsonSettingsFile
from tests.applications.browser.browser_services import BrowserServices


class TestWithBrowser:
    test_site: str = "http://the-internet.herokuapp.com"

    service_provider: ServiceProvider = None

    def setup_method(self):
        self.service_provider = CustomStartup.configure_services(lambda: BrowserServices.Instance.application)
        BrowserServices.Instance.service_provider = self.service_provider

    def teardown_method(self):
        if BrowserServices.Instance.is_application_started():
            BrowserServices.Instance.application.quit()

    def go_to_url(self, url: str, driver: WebDriver = None):
        driver_instance = driver or BrowserServices.Instance.application.driver
        try:
            driver_instance.get(url)
        except WebDriverException as e:
            if driver_instance.current_url:
                Logger.fatal(f"Random error occurred: [{e.msg}], but successfully navigated to URL [{url}]")
            else:
                raise e


class CustomStartup(Startup):
    @classmethod
    def configure_services(
        cls,
        application_provider: Callable,
        settings: Optional[JsonSettingsFile] = None,
        service_provider: Optional[ServiceProvider] = None,
    ) -> ServiceProvider:
        service_provider = super().configure_services(application_provider, settings)
        return service_provider
