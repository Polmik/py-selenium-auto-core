import abc

from selenium.webdriver.remote.webdriver import WebDriver


class Application(abc.ABC):
    """Interface of any application controlled by Selenium WebDriver API"""

    @property
    @abc.abstractmethod
    def driver(self) -> WebDriver:
        """Current instance of driver"""
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def is_started(self) -> bool:
        """Defines if the application is already started or not."""
        raise NotImplementedError("Abstract")

    @abc.abstractmethod
    def set_implicit_wait_timeout(self, timeout: float):
        """Sets implicit wait timeout to browser.
        Method was extracted with purpose not to pass it to Driver if it is similar to previous value.
        Simplest implementation is: driver.implicitly_wait(timeout)

        Args:
            timeout: timeout to set
        """
        raise NotImplementedError("Abstract")
