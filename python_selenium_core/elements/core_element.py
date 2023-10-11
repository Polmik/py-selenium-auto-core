import abc
from typing import Any, Callable

from selenium.common import WebDriverException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement

from python_selenium_core.applications.application import Application
from python_selenium_core.configurations.element_cache_configuration import ElementCacheConfiguration
from python_selenium_core.configurations.logger_configuration import LoggerConfiguration
from python_selenium_core.elements.constants.element_state import ElementState
from python_selenium_core.elements.element_cache_handler import ElementCacheHandler
from python_selenium_core.elements.element_factory import ElementFactory
from python_selenium_core.elements.element_finder import ElementFinder
from python_selenium_core.elements.element_state_provider import ElementStateProvider
from python_selenium_core.localization.localization_manager import LocalizationManager
from python_selenium_core.localization.localized_logger import LocalizedLogger
from python_selenium_core.locator.locator import Locator
from python_selenium_core.logging.logger import Logger
from python_selenium_core.utilities.action_retrier import ActionRetrier
from python_selenium_core.waitings.conditional_wait import ConditionalWait


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
    def application(self) -> Application:
        raise NotImplementedError("Abstract")

    @property
    @abc.abstractmethod
    def action_retrier(self) -> ActionRetrier:
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
    def factory(self) -> ElementFactory:
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
                self.localization_manager.get_localized_message(state_key)
            )

        return predicate

    def click(self):
        self.log_element_action("loc.clicking")
        self.do_with_retry(lambda: self.get_element().click())

    def find_child_element(self):
        raise NotImplementedError

    def find_child_elements(self):
        raise NotImplementedError

    def get_attribute(self, attr) -> str:
        self.log_element_action("loc.el.getattr", attr)
        value = self.do_with_retry(lambda: self.get_element().get_attribute(attr))
        self.log_element_action("loc.el.attr.value", attr, value)
        return value

    def get_element(self, timeout: float = None) -> WebElement:
        try:
            if self.cache_configuration.is_enabled:
                return self.cache.get_element(timeout)
            return self.finder.find_element(
                locator=self.locator,
                state=self.element_state,
                timeout=timeout,
                name=self.name
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
        self.log_element_action("loc.get.text")
        text = self.do_with_retry(lambda: self.get_element().text)
        self.log_element_action("loc.text.value", text)
        return text

    def send_keys(self, value) -> None:
        self.log_element_action("loc.text.sending.keys", value)
        self.do_with_retry(lambda: self.get_element().send_keys(value))

    def do_with_retry(self, function) -> Any:
        return self.action_retrier.do_with_retry(function)

    def log_element_action(self, message_key: str, *args):
        self.localized_logger.info_element_action(self.element_type, self.name, message_key, args)
