from typing import Callable

from python_selenium_core.elements.element_cache_handler import ElementCacheHandler
from python_selenium_core.locator.locator import Locator
from python_selenium_core.waitings.conditional_wait import ConditionalWait


class CachedElementStateProvider:

    def __init__(
            self,
            locator: Locator,
            conditional_wait: ConditionalWait,
            element_cache_handler: ElementCacheHandler,
            log_element_state: Callable[[str, str], None]
    ):
        self.__locator = locator
        self.__conditional_wait = conditional_wait
        self.__element_cache_handler = element_cache_handler
        self.__log_element_state = log_element_state
