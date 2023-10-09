import abc

from selenium.webdriver.remote.webdriver import WebDriver

from core.applications.startup import Startup


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
    def set_implicit_wait_timeout(self):
        raise NotImplementedError("Abstract")


#class CoreService(Application):
class CoreService:

    _app_container: Application = None
    _startup_container: Startup = None

    @staticmethod
    def _is_application_started() -> bool:
        return CoreService._app_container is not None and CoreService._app_container.is_started

    @staticmethod
    def set_startup(startup: Startup):
        CoreService._startup_container = startup

    @staticmethod
    def get_startup() -> Startup:
        if CoreService._startup_container is None:
            CoreService._startup_container = Startup
        return CoreService._startup_container



