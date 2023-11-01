import logging

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from py_selenium_auto_core.applications.application import Application
from py_selenium_auto_core.configurations.timeout_configuration import TimeoutConfiguration


class ChromeApplication(Application):

    def __init__(self, timeout_configuration: TimeoutConfiguration):
        for log_name in [
            'selenium.webdriver.remote.remote_connection',
            'selenium.webdriver.common.selenium_manager',
            'urllib3.connectionpool',
        ]:
            logger = logging.getLogger(log_name)
            logger.disabled = True
        options = Options()
        service = Service()
        driver_manager = ChromeDriverManager(driver_version=None)
        service.path = driver_manager.install()
        options.headless = True
        self._driver = WebDriver(options=options, service=service)
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
