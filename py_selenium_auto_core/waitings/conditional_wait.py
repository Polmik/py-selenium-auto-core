import time
from time import sleep
from typing import Any, Callable, List, TYPE_CHECKING

from selenium.common import StaleElementReferenceException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from py_selenium_auto_core.configurations.timeout_configuration import (
    TimeoutConfiguration,
)

if TYPE_CHECKING:
    from py_selenium_auto_core.applications.startup import ServiceProvider


class ConditionalWait:
    """This class is used for waiting any conditions."""

    def __init__(
        self,
        timeout_configuration: TimeoutConfiguration,
        service_provider: "ServiceProvider",
    ):
        """ConditionalWait constructor

        Args:
            timeout_configuration (TimeoutConfiguration): Timeout configurations
            service_provider (ServiceProvider): Dependency container
        """
        self._timeout_configuration = timeout_configuration
        self._service_provider = service_provider

    def wait_for_driver(
        self,
        function: Callable[[WebDriver], Any],
        timeout: float = None,
        polling_interval: float = None,
        message: str = None,
        exceptions_to_ignore: List = None,
    ) -> Any:
        """Wait for some object from condition with timeout using Selenium WebDriver.

        Args:
            function: Predicate for waiting
            timeout: Condition timeout. Default value is TimeoutConfiguration.condition
            polling_interval: Condition check interval. Default value is TimeoutConfiguration.polling_interval
            message: Part of error message in case of Timeout exception
            exceptions_to_ignore: Possible exceptions that have to be ignored.
                Handles StaleElementReferenceException by default.

        Returns:
            Condition result which is waiting for.

        Exception:
            WebDriverTimeoutException: Throws when timeout exceeded and condition not satisfied.
        """
        ignore_exceptions = exceptions_to_ignore or [StaleElementReferenceException]
        wait_timeout = self._resolve_condition_timeout(timeout)
        check_interval = self._resolve_polling_interval(polling_interval)
        application = self._service_provider.application()
        application.set_implicit_wait_timeout(0)
        wait = WebDriverWait(
            driver=application.driver,
            timeout=wait_timeout,
            poll_frequency=check_interval,
            ignored_exceptions=ignore_exceptions,
        )

        result = wait.until(function, self.__get_timeout_exception_message(wait_timeout, message))
        application.set_implicit_wait_timeout(self._timeout_configuration.implicit)
        return result

    def wait_for_condition(
        self,
        function: Callable[[], bool],
        timeout: float = None,
        polling_interval: float = None,
        exceptions_to_ignore: list = None,
    ) -> bool:
        """Wait for some condition within timeout.

        Args:
            function: Predicate for waiting
            timeout: Condition timeout. Default value is TimeoutConfiguration.condition
            polling_interval: Condition check interval. Default value is TimeoutConfiguration.polling_interval
            exceptions_to_ignore: Possible exceptions that have to be ignored

        Returns:
            True if condition satisfied and false otherwise.
        """

        def _predicate() -> bool:
            self.wait_for_true(
                function=function,
                timeout=timeout,
                polling_interval=polling_interval,
                exceptions_to_ignore=exceptions_to_ignore,
            )
            return True

        return self._is_condition_satisfied(
            function=_predicate,
            exceptions_to_ignore=[TimeoutException],
        )

    def wait_for_true(
        self,
        function: Callable[[], bool],
        timeout: float = None,
        polling_interval: float = None,
        message: str = None,
        exceptions_to_ignore: list = None,
    ) -> None:
        """Wait for some condition within timeout.

        Args:
            function: Predicate for waiting
            timeout: Condition timeout. Default value is TimeoutConfiguration.condition
            polling_interval: Condition check interval. Default value is TimeoutConfiguration.polling_interval
            message: Part of error message in case of Timeout exception
            exceptions_to_ignore: Possible exceptions that have to be ignored

        Exception:
            TimeoutException: Throws exception when timeout exceeded and condition not satisfied
        """
        if function is None:
            raise ValueError("Function cannot be None")

        wait_timeout = self._resolve_condition_timeout(timeout)
        check_interval = self._resolve_polling_interval(polling_interval)
        start_time = time.time()
        while True:
            if self._is_condition_satisfied(function, exceptions_to_ignore or []):
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
    def _is_condition_satisfied(function: Callable[[], bool], exceptions_to_ignore: List) -> bool:
        try:
            return function()
        except Exception as ex:
            if ConditionalWait._is_ignored_exception(ex, exceptions_to_ignore):
                return False
            raise ex

    def _resolve_condition_timeout(self, timeout: float) -> float:
        return self._timeout_configuration.condition if timeout is None else timeout

    def _resolve_polling_interval(self, polling_interval: float) -> float:
        return self._timeout_configuration.polling_interval if polling_interval is None else polling_interval

    @staticmethod
    def _is_ignored_exception(ex: Exception, exceptions_to_ignore: List) -> bool:
        return any(map(lambda ex_to_ignore: isinstance(ex, ex_to_ignore), exceptions_to_ignore))
