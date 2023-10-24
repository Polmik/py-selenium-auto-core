import time
from time import sleep
from typing import Any, Callable, List

from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from python_selenium_core.configurations.timeout_configuration import TimeoutConfiguration


class ConditionalWait:

    def __init__(self, timeout_configuration: TimeoutConfiguration, service_provider):
        self.__timeout_configuration = timeout_configuration
        self.__service_provider = service_provider

    def wait_for_driver(
            self,
            function: Callable[[WebDriver], Any],
            timeout: float = None,
            polling_interval: float = None,
            message: str = None,
            exceptions_to_ignore: List = None
    ) -> Any:
        ignore_exceptions = exceptions_to_ignore or [StaleElementReferenceException]
        wait_timeout = self.__resolve_condition_timeout(timeout)
        check_interval = self.__resolve_polling_interval(polling_interval)
        application = self.__service_provider.application()
        application.set_implicit_wait_timeout(0)
        wait = WebDriverWait(
            driver=application.driver,
            timeout=wait_timeout,
            poll_frequency=check_interval,
            ignored_exceptions=ignore_exceptions,
        )

        result = wait.until(function, self.__get_timeout_exception_message(wait_timeout, message))
        application.set_implicit_wait_timeout(self.__timeout_configuration.implicit)
        return result

    def wait_for_condition(
            self,
            function: Callable[[], bool],
            timeout: float = None,
            polling_interval: float = None,
            exceptions_to_ignore: list = None
    ) -> bool:
        def predicate() -> bool:
            self.wait_for_true(
                function=function,
                timeout=timeout,
                polling_interval=polling_interval,
                exceptions_to_ignore=exceptions_to_ignore,
            )
            return True

        return self.__is_condition_satisfied(
            function=predicate,
            exceptions_to_ignore=[TimeoutException],
        )

    def wait_for_true(
            self,
            function: Callable[[], bool],
            timeout: float = None,
            polling_interval: float = None,
            message: str = None,
            exceptions_to_ignore: list = None
    ):
        if function is None:
            raise ValueError("Function cannot be None")

        wait_timeout = self.__resolve_condition_timeout(timeout)
        check_interval = self.__resolve_polling_interval(polling_interval)
        start_time = time.time()
        while True:
            if self.__is_condition_satisfied(function, exceptions_to_ignore or []):
                return
            if time.time() - start_time > wait_timeout:
                raise TimeoutException(self.__get_timeout_exception_message(wait_timeout, message))
            sleep(check_interval)

    @staticmethod
    def __get_timeout_exception_message(wait_timeout: float, message: str = None) -> str:
        exception_message = f"Timed out after {wait_timeout} seconds"
        if message is not None:
            exception_message += f": {message}"
        return exception_message

    @staticmethod
    def __is_condition_satisfied(
            function: Callable[[], bool],
            exceptions_to_ignore: List
    ) -> bool:
        try:
            return function()
        except Exception as ex:
            if ConditionalWait._is_ignored_exception(ex, exceptions_to_ignore):
                return False
            raise ex

    def __resolve_condition_timeout(self, timeout: float) -> float:
        return self.__timeout_configuration.condition if timeout is None else timeout

    def __resolve_polling_interval(self, polling_interval: float) -> float:
        return self.__timeout_configuration.polling_interval if polling_interval is None else polling_interval

    @staticmethod
    def _is_ignored_exception(ex: Exception, exceptions_to_ignore: List) -> bool:
        return any(map(lambda exti: isinstance(ex, exti), exceptions_to_ignore))