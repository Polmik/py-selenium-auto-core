from selenium.webdriver.chrome.webdriver import WebDriver

from core.applications.application import Application
from core.configurations.timeout_configuration import TimeoutConfiguration


class ChromeApplication(Application):

    def __init__(self, timeout_configuration: TimeoutConfiguration):
        self._driver = WebDriver()
        self.implicit_wait = timeout_configuration.implicit
        self.driver.implicitly_wait(self.implicit_wait)

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @property
    def is_started(self) -> bool:
        return self.driver.session_id is not None

    def set_implicit_wait_timeout(self, timeout: float):
        if timeout != self.implicit_wait:
            self.implicit_wait = timeout
            self.driver.implicitly_wait(self.implicit_wait)

    def quit(self):
        if self.driver is not None:
            self.driver.quit()