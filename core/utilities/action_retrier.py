from time import sleep
from typing import Any, Callable

from core.configurations.retry_configuration import RetryConfiguration


class ActionRetrier:

    def __init__(self, retry_configuration: RetryConfiguration):
        self.retry_configuration = retry_configuration

    def do_with_retry(self, function: Callable, handled_exceptions=None) -> Any:
        exceptions_to_handle = handled_exceptions if handled_exceptions is not None else []
        retry_attempts_left = self.retry_configuration.number
        actual_interval = self.retry_configuration.polling_interval
        result = None

        while retry_attempts_left >= 0:
            try:
                result = function()
                break
            except Exception as e:
                if retry_attempts_left != 0 and e in exceptions_to_handle:
                    sleep(actual_interval)
                    retry_attempts_left -= 1
                else:
                    raise e
        return result
