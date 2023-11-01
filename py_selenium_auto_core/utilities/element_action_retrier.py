from typing import Callable, Optional, Any

from selenium.common import StaleElementReferenceException, InvalidElementStateException

from py_selenium_auto_core.configurations.retry_configuration import RetryConfiguration
from py_selenium_auto_core.utilities.action_retrier import ActionRetrier


class ElementActionRetrier(ActionRetrier):
    """This class is used for do some action with retry when HandledExceptions occures"""

    def __init__(self, retry_configuration: RetryConfiguration):
        """RetryConfiguration constructor

        Args:
            retry_configuration (RetryConfiguration): Retry configurations
        """
        super().__init__(retry_configuration)

        """Exceptions to be ignored during action retrying"""
        self.handled_exceptions = [
            StaleElementReferenceException,
            InvalidElementStateException,
        ]

    def do_with_retry(self, function: Callable, handled_exceptions: Optional[list] = None) -> Any:
        return super().do_with_retry(function, handled_exceptions or self.handled_exceptions)
