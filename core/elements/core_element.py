import abc
import logging
from typing import Any

from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from core.configurations.element_cache_configuration import ElementCacheConfiguration
from core.elements.constants.element_state import ElementState
from core.elements.element_cache_handler import ElementCacheHandler
from core.elements.element_finder import ElementFinder
from core.elements.element_state_provider import ElementStateProvider
from core.locator.locator import Locator
from core.utilities.action_retrier import ActionRetrier
from core.waitings.conditional_wait import ConditionalWait


class CoreElement(abc.ABC):
    _element_cache_handler: ElementCacheHandler = None

    def __init__(self, locator: Locator, name: str, element_state: ElementState):
        self.locator = locator
        self.name = name
        self.element_state = element_state

    @property
    def state(self):
        if self.cache_configuration.is_enabled:
            raise NotImplementedError
        return ElementStateProvider(self.locator, self.conditional_wait, self.finder)

    @property
    def visual(self):
        raise NotImplementedError

    @property
    def cache(self) -> ElementCacheHandler:
        if self._element_cache_handler is None:
            self._element_cache_handler = ElementCacheHandler(self.locator, self.name, self.element_state, self.finder)
        return self._element_cache_handler

    @property
    @abc.abstractmethod
    def action_retrier(self) -> ActionRetrier:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def cache_configuration(self) -> ElementCacheConfiguration:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def conditional_wait(self) -> ConditionalWait:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def element_type(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def factory(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def finder(self) -> ElementFinder:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def image_comparator(self):
        raise NotImplementedError

    def click(self):
        self.log_element_action(f"Clicking on {self.name}")
        self.do_with_retry(lambda: self.get_element().click())

    def find_child_element(self):
        raise NotImplementedError

    def find_child_elements(self):
        raise NotImplementedError

    def get_attribute(self, attr):
        self.log_element_action(f"Getting attribute '{attr}' from {self.name}")
        value = self.do_with_retry(lambda: self.get_element().get_attribute(attr))
        self.log_element_action(f"Value of attribute '{attr}': [{value}]")
        return value

    def get_element(self, timeout=None) -> WebElement:
        try:
            if self.cache_configuration.is_enabled:
                raise NotImplementedError("No implementation for cache")
            return self.finder.find_element(
                locator=self.locator,
                state=self.element_state,
                timeout=timeout,
                name=self.name
            )
        except NoSuchElementException as e:
            self.log_page_source(e)
            raise e

    def get_elements(self, timeout=None) -> WebElement:
        try:
            if self.cache_configuration.is_enabled:
                raise NotImplementedError("No implementation for cache")
            return self.finder.find_elements(
                locator=self.locator,
                state=self.element_state,
                timeout=timeout,
                name=self.name
            )
        except NoSuchElementException as e:
            self.log_page_source(e)
            raise e

    def log_page_source(self, exception: WebDriverException):
        try:
            logging.debug(f"Page source:{self.__browser.driver.page_source}", exc_info=exception)
        except WebDriverException as e:
            logging.error(e.msg)
            logging.debug("An exception occurred while tried to save the page source", exc_info=e)

    @property
    def text(self) -> str:
        self.log_element_action(f"Getting text from element {self.name}")
        text = self.do_with_retry(lambda: self.get_element().text)
        self.log_element_action(f"Element's text: [{text}]")
        return text

    def send_keys(self, value) -> None:
        self.log_element_action(f"Setting text for element {self.name}")
        self.log_element_action(f"Sending keys '{value}'")
        self.do_with_retry(lambda: self.get_element().send_keys(value))

    def do_with_retry(self, function) -> Any:
        return self.action_retrier.do_with_retry(function)

    def log_element_action(self, message):
        is_debug = False
        logger = logging.debug if is_debug else logging.info
        logger(f"Element {self.name}: {message}")
