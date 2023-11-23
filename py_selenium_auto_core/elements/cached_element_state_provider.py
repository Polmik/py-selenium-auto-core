from typing import Callable

from py_selenium_auto_core.elements.element_cache_handler import ElementCacheHandler
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait


class CachedElementStateProvider:
    def __init__(
        self,
        locator: Locator,
        conditional_wait: ConditionalWait,
        element_cache_handler: ElementCacheHandler,
        log_element_state: Callable[[str, str], None],
    ):
        self._locator = locator
        self._conditional_wait = conditional_wait
        self._element_cache_handler = element_cache_handler
        self._log_element_state = log_element_state
