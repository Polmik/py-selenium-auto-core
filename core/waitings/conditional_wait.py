import time
from time import sleep
from typing import Any, Callable

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from core.configurations.timeout_configuration import TimeoutConfiguration


class ConditionalWait:

    def __init__(self, timeout_configuration: TimeoutConfiguration, application):
        self.__timeout_configuration = timeout_configuration
        self.__application = application

    @property
    def browser(self):
        # TODO Обходное решение, чтоюы передать инстанс приложения для установки таймаутов
        exec('import framework')
        return eval("framework.BrowserServiceInstance.browser")

    def wait_for_driver(
            self,
            function: Callable[[WebDriver], Any],
            timeout: int = None,
            polling_interval: int = None,
            message: str = None,
            exceptions_to_ignore: list = None
    ) -> Any:
        exceptions_to_ignore = exceptions_to_ignore or []
        application = self.__application
        application.set_implicit_wait_timeout(0)
        wait_timeout = self.__resolve_condition_timeout(timeout)
        check_interval = self.__resolve_polling_interval(polling_interval)
        wait = WebDriverWait(
            driver=application.driver,
            timeout=wait_timeout,
            poll_frequency=check_interval,
            ignored_exceptions=exceptions_to_ignore,
        )

        result = wait.until(function, f"Timed out after {wait_timeout} seconds: {message}")
        application.set_implicit_wait_timeout(self.__timeout_configuration.implicit)
        return result

    def wait_for_condition(
            self,
            function: Callable[[], bool],
            timeout: float = None,
            polling_interval: int = None,
            exceptions_to_ignore: list = None
    ) -> bool:
        def condition() -> bool:
            self.wait_for_true(
                function=function,
                timeout=timeout,
                polling_interval=polling_interval,
                exceptions_to_ignore=exceptions_to_ignore,
            )
            return True

        return self.__is_condition_satisfied(
            function=condition,
            exceptions_to_ignore=list(),
        )

    def wait_for_true(
            self,
            function: Callable[[], bool],
            timeout: float = None,
            polling_interval: int = None,
            message: str = None,
            exceptions_to_ignore: list = None
    ):
        if function is None:
            raise ValueError("Value is not be None")

        wait_timeout = self.__resolve_condition_timeout(timeout)
        check_interval = self.__resolve_polling_interval(polling_interval)
        start_time = time.time()
        exceptions_to_ignore = exceptions_to_ignore or []
        while True:
            if self.__is_condition_satisfied(function, exceptions_to_ignore):
                return
            if time.time() - start_time > wait_timeout:
                raise self.__get_timeout_exception(wait_timeout, message)
            sleep(check_interval)

    @staticmethod
    def __get_timeout_exception(wait_timeout: int, message: str = None) -> TimeoutError:
        exception_message = f"Timed out after {wait_timeout} seconds"
        if message is not None:
            exception_message += f": {message}"
        return TimeoutError(exception_message)

    @staticmethod
    def __is_condition_satisfied(
            function: Callable[[], bool],
            exceptions_to_ignore: list
    ) -> bool:
        try:
            return function()
        except Exception as e:
            if type(e) in exceptions_to_ignore:
                return False
            raise e

    def __resolve_condition_timeout(self, timeout):
        return self.__timeout_configuration.condition if timeout is None else timeout

    def __resolve_polling_interval(self, polling_interval):
        return self.__timeout_configuration.polling_interval if polling_interval is None else polling_interval
