from py_selenium_auto_core.applications.core_services import CoreServices
from py_selenium_auto_core.applications.startup import ServiceProvider
from tests.applications.browser.chrome_application import ChromeApplication


class BrowserServices:

    class BrowserServiceInstance(CoreServices):

        def is_application_started(self) -> bool:
            return self._is_application_started()

        @property
        def application(self) -> ChromeApplication:
            return self._get_application(lambda services: self._start_chrome(services))

        @property
        def service_provider(self) -> ServiceProvider:
            return self._get_service_provider(lambda services: self.application)

        @service_provider.setter
        def service_provider(self, value: ServiceProvider):
            self._set_service_provider(value)

        @staticmethod
        def _start_chrome(service_provider: ServiceProvider):
            return ChromeApplication(service_provider.timeout_configuration())

    Instance: BrowserServiceInstance = BrowserServiceInstance()
