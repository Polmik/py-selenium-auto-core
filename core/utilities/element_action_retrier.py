from typing import Callable, Optional, Any

from selenium.common import StaleElementReferenceException, InvalidElementStateException

from core.configurations.retry_configuration import RetryConfiguration
from core.utilities.action_retrier import ActionRetrier


class ElementActionRetrier(ActionRetrier):

    def __init__(self, retry_configuration: RetryConfiguration):
        super().__init__(retry_configuration)
        self.handled_exceptions = [
            StaleElementReferenceException,
            InvalidElementStateException,
        ]

    def do_with_retry(self, function: Callable, handled_exceptions: Optional[list] = None) -> Any:
        return super().do_with_retry(function, handled_exceptions or self.handled_exceptions)
