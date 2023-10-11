import logging

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from core.applications.application import Application
from core.configurations.timeout_configuration import TimeoutConfiguration


class ChromeApplication(Application):

    def __init__(self, timeout_configuration: TimeoutConfiguration):
        for log_name in [
            'selenium.webdriver.remote.remote_connection',
            'urllib3.connectionpool',
        ]:
            logger = logging.getLogger(log_name)
            logger.disabled = True
        options = Options()
        options.headless = False
        self._driver = WebDriver(options=options)
        self.implicit_wait = timeout_configuration.implicit
        self.driver.implicitly_wait(self.implicit_wait)

    @property
    def driver(self) -> WebDriver:
        return self._driver

    @property
    def is_started(self) -> bool:
        return self.driver is not None and self.driver.session_id is not None

    def set_implicit_wait_timeout(self, timeout: float):
        if timeout != self.implicit_wait:
            self.implicit_wait = timeout
            self.driver.implicitly_wait(self.implicit_wait)

    def quit(self):
        if self.driver is not None:
            self.driver.quit()
        self.driver.session_id = None
