import abc
from typing import Any, Callable, Optional, TYPE_CHECKING, Type, TypeVar, List

from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from py_selenium_auto_core.applications.application import Application
from py_selenium_auto_core.configurations.element_cache_configuration import (
    ElementCacheConfiguration,
)
from py_selenium_auto_core.configurations.logger_configuration import (
    LoggerConfiguration,
)
from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.elements.constants.elements_count import ElementsCount
from py_selenium_auto_core.elements.element_cache_handler import ElementCacheHandler

from py_selenium_auto_core.elements.element_finder import ElementFinder
from py_selenium_auto_core.elements.element_state_provider import ElementStateProvider
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.action_retrier import ActionRetrier
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait

if TYPE_CHECKING:
    from py_selenium_auto_core.elements.element_factory import ElementFactory

T = TypeVar("T", bound="CoreElement", covariant=True)


class CoreElement(abc.ABC):
    """Describes behavior of any UI element"""

    def __init__(self, locator: Locator, name: str, element_state: ElementState):
        """CoreElement constructor

        Args:
            locator: Unique locator of element
            name: Unique name of element
            element_state: Element state
        """
        self.locator = locator
        self.name = name
        self._element_state = element_state
        self._element_cache_handler: Optional[ElementCacheHandler] = None

    @property
    def state(self):
        """Gets element state"""
        if self.cache_configuration.is_enabled:
            raise NotImplementedError
        return ElementStateProvider(self.locator, self.conditional_wait, self.finder, self.log_element_state)

    @property
    def visual(self):
        """Gets element visual state"""
        raise NotImplementedError

    @property
    def cache(self) -> ElementCacheHandler:
        """Gets element cache handler"""
        if self._element_cache_handler is None:
            self._element_cache_handler = ElementCacheHandler(self.locator, self.name, self._element_state, self.finder)
        return self._element_cache_handler

    @property
    @abc.abstractmethod
    def action_retrier(self) -> ActionRetrier:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def application(self) -> Application:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def cache_configuration(self) -> ElementCacheConfiguration:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def conditional_wait(self) -> ConditionalWait:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def element_type(self) -> str:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def factory(self) -> "ElementFactory":
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def finder(self) -> ElementFinder:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def image_comparator(self):
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def localized_logger(self) -> LocalizedLogger:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def localization_manager(self) -> LocalizationManager:
        raise NotImplementedError("Abstract")

    @property
    def logger_configuration(self) -> LoggerConfiguration:
        return self.localized_logger.configuration

    @property
    def logger(self) -> Logger:
        return Logger()

    @property
    def log_element_state(self) -> Callable[[str, str], None]:
        def predicate(message_key: str, state_key: str):
            self.localized_logger.info_element_action(
                self.element_type,
                self.name,
                message_key,
                self.localization_manager.get_localized_message(state_key),
            )

        return predicate

    def click(self):
        """Clicks the element"""
        self.log_element_action("loc.clicking")
        self.do_with_retry(lambda: self.get_element().click())

    def find_child_element(
        self,
        element_type: Type[T],
        child_locator: Locator,
        name: str = None,
        state: ElementState = ElementState.Displayed,
    ) -> T:
        """Finds child element by its locator relative to parent element

        Args:
            element_type: Type of the element to create
            child_locator: Locator of child element relative to its parent
                Supports:
                    Locator(By.XPATH, "./div") or Locator(By.XPATH, "/div") or Locator(By.XPATH, "/div[@id]")
                    Locator(By.XPATH, ".//div") or Locator(By.XPATH, "//div") or Locator(By.XPATH, "//div[@id]")
                    Locator(By.XPATH, "div") or Locator(By.XPATH, "div[@id]")
                    Locator(By.CLASS_NAME, "class_name")
                    Locator(By.TAG_NAME, "tag_name")
            name: Child element name
            state: Child element state

        Returns:
            Instance of child element
        """
        return self.factory.find_child_element(element_type, self, child_locator, name, state)

    def find_child_elements(
        self,
        element_type: Type[T],
        child_locator: Locator,
        name: str = None,
        expected_count: ElementsCount = ElementsCount.Any,
        state: ElementState = ElementState.Displayed,
    ) -> List[T]:
        """Finds list of child elements by their locator relative to parent element

        Args:
            element_type: Type of the element to create
            child_locator: Locator of child elements relative to their parent
                Supports:
                    Locator(By.XPATH, "./div") or Locator(By.XPATH, "/div") or Locator(By.XPATH, "/div[@id]")
                    Locator(By.XPATH, ".//div") or Locator(By.XPATH, "//div") or Locator(By.XPATH, "//div[@id]")
                    Locator(By.XPATH, "div") or Locator(By.XPATH, "div[@id]")
                    Locator(By.CLASS_NAME, "class_name")
                    Locator(By.TAG_NAME, "tag_name")
            name: Child elements name
            expected_count: Expected number of elements that have to be found (zero, more then zero, any)
            state: Child elements state

        Returns:
            List of child elements
        """
        return self.factory.find_child_elements(element_type, self, child_locator, name, expected_count, state)

    def get_attribute(self, attr) -> str:
        """Gets element attribute value by its name"""
        self.log_element_action("loc.el.getattr", attr)
        value = self.do_with_retry(lambda: self.get_element().get_attribute(attr))
        self.log_element_action("loc.el.attr.value", attr, value)
        return value

    def get_element(self, timeout: float = None) -> WebElement:
        """Finds current element by specified locator

        Args:
            timeout: Timeout to find element. Default: Configurations.TimeoutConfiguration.condition

        Returns:
            Instance of WebElement if found

        Exception:
            NoSuchElementException: Thrown when no elements found
        """
        try:
            if self.cache_configuration.is_enabled:
                return self.cache.get_element(timeout)
            return self.finder.find_element(
                locator=self.locator,
                state=self._element_state,
                timeout=timeout,
                name=self.name,
            )
        except NoSuchElementException as e:
            if self.logger_configuration.log_page_source:
                self.log_page_source(e)
            raise e

    def log_page_source(self, exception: WebDriverException):
        try:
            self.logger.debug(f"Page source:{self.application.driver.page_source}", exc_info=exception)
        except WebDriverException as e:
            self.logger.error(e.msg)
            self.logger.debug("An exception occurred while tried to save the page source", exc_info=e)

    @property
    def text(self) -> str:
        """Gets element text"""
        self.log_element_action("loc.get.text")
        text = self.do_with_retry(lambda: self.get_element().text)
        self.log_element_action("loc.text.value", text)
        return text

    def send_keys(self, value) -> None:
        """Sends keys to element"""
        self.log_element_action("loc.text.sending.keys", value)
        self.do_with_retry(lambda: self.get_element().send_keys(value))

    def do_with_retry(self, function) -> Any:
        return self.action_retrier.do_with_retry(function)

    def log_element_action(self, message_key: str, *args):
        self.localized_logger.info_element_action(self.element_type, self.name, message_key, *args)
