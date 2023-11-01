from time import sleep
from typing import Any, Callable

from py_selenium_auto_core.configurations.retry_configuration import RetryConfiguration


class ActionRetrier:
    """This class is used for do some action with retry."""

    def __init__(self, retry_configuration: RetryConfiguration):
        """RetryConfiguration constructor

        Args:
            retry_configuration (RetryConfiguration): Retry configurations
        """
        self.__retry_configuration = retry_configuration

    def do_with_retry(self, function: Callable, handled_exceptions: list = None) -> Any:
        """Retries the action when one of the handledExceptions occures.

        Args:
            function: Action to be applied
            handled_exceptions: Exceptions to be handled

        Returns:
            Condition result which is waiting for.

        Exception:
            WebDriverTimeoutException: Throws when timeout exceeded and condition not satisfied.
        """
        exceptions_to_handle = handled_exceptions if handled_exceptions is not None else []
        retry_attempts_left = self.__retry_configuration.number
        actual_interval = self.__retry_configuration.polling_interval
        result = None

        while retry_attempts_left >= 0:
            try:
                result = function()
                break
            except Exception as e:
                if retry_attempts_left != 0 and self._is_ignored_exception(e, exceptions_to_handle):
                    sleep(actual_interval)
                    retry_attempts_left -= 1
                else:
                    raise e
        return result

    @staticmethod
    def _is_ignored_exception(ex: Exception, exceptions_to_ignore: list) -> bool:
        return any(map(lambda exti: isinstance(ex, exti), exceptions_to_ignore))
