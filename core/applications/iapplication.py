import abc

from selenium.webdriver.remote.webdriver import WebDriver


class Application(abc.ABC):

    @property
    @abc.abstractmethod
    def driver(self) -> WebDriver:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def is_started(self) -> bool:
        raise NotImplementedError("Abstract")

    @abc.abstractmethod
    def set_implicit_wait_timeout(self, timeout: float):
        raise NotImplementedError("Abstract")
