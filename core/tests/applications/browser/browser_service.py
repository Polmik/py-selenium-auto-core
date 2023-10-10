from core.applications.core_service import CoreService
from core.applications.startup import ServiceProvider
from core.tests.applications.browser.chrome_application import ChromeApplication


class BrowserService(CoreService):

    @staticmethod
    def is_application_started() -> bool:
        return CoreService._is_application_started()

    @staticmethod
    def application() -> ChromeApplication:
        return CoreService.get_application(lambda service: BrowserService._start_chrome(service))

    @staticmethod
    def service_provider() -> ServiceProvider:
        return CoreService.get_service_provider(lambda service: BrowserService.application())

    @staticmethod
    def _start_chrome(service_provider: ServiceProvider):
        return ChromeApplication(service_provider.timeout_configuration())
