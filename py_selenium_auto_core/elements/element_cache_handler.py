from typing import Optional

from selenium.webdriver.remote.webelement import WebElement

from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.elements.element_finder import ElementFinder
from py_selenium_auto_core.locator.locator import Locator


class ElementCacheHandler:
    """Allows to use cached element"""

    def __init__(self, locator: Locator, name: str, state: ElementState, finder: ElementFinder):
        self._locator = locator
        self._name = name
        self._state = state
        self._element_finder = finder
        self._element: Optional[WebElement] = None

    @property
    def is_stale(self) -> bool:
        """Determines is the element stale"""
        return self._element is not None and self.is_refresh_needed()

    def is_refresh_needed(self, custom_sate: ElementState = None) -> bool:
        """Determines is the cached element refresh needed

        Args:
            custom_sate: Custom element's existance state used for search
        """
        if self._element is None:
            return True
        try:
            is_displayed = self._element.is_displayed()
            # refresh is needed only if the property is not match to expected element state
            return (self._state if custom_sate is None else custom_sate) == self._state.Displayed and not is_displayed
        except Exception:
            # refresh is needed if the property is not available
            return True

    def get_element(self, timeout: float = None, custom_sate: ElementState = None) -> WebElement:
        """Allows to get cached element

        Args:
            timeout: Timeout used to retrive the element when is_refresh_needed(ElementState?)" is true
            custom_sate: Custom element's existance state used for search

        Returns:
            Cached element
        """
        if self.is_refresh_needed(custom_sate):
            self._element = self._element_finder.find_element(
                locator=self._locator,
                state=self._state if custom_sate is None else custom_sate,
                timeout=timeout,
                name=self._name,
            )
        return self._element
