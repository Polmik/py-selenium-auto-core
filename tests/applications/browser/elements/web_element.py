import abc

from py_selenium_auto_core.elements.core_element import CoreElement
from py_selenium_auto_core.applications.application import Application
from py_selenium_auto_core.configurations.element_cache_configuration import (
    ElementCacheConfiguration,
)
from py_selenium_auto_core.configurations.logger_configuration import (
    LoggerConfiguration,
)
from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.elements.element_cache_handler import ElementCacheHandler
from py_selenium_auto_core.elements.element_factory import ElementFactory
from py_selenium_auto_core.elements.element_finder import ElementFinder
from py_selenium_auto_core.elements.element_state_provider import ElementStateProvider
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.action_retrier import ActionRetrier
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait
from tests.applications.browser.browser_services import BrowserServices


class WebElement(CoreElement, abc.ABC):
    def __init__(self, locator: Locator, name: str, element_state: ElementState):
        super().__init__(locator, name, element_state)

    @property
    def action_retrier(self) -> ActionRetrier:
        return BrowserServices.Instance.service_provider.action_retrier()

    @property
    def application(self) -> Application:
        return BrowserServices.Instance.application

    @property
    def cache_configuration(self) -> ElementCacheConfiguration:
        return BrowserServices.Instance.service_provider.element_cache_configuration()

    @property
    def conditional_wait(self) -> ConditionalWait:
        return BrowserServices.Instance.service_provider.conditional_wait()

    @property
    def factory(self) -> ElementFactory:
        return BrowserServices.Instance.service_provider.element_factory()

    @property
    def finder(self) -> ElementFinder:
        return BrowserServices.Instance.service_provider.element_finder()

    @property
    def image_comparator(self):
        raise NotImplementedError("Abstract")

    @property
    def localized_logger(self) -> LocalizedLogger:
        return BrowserServices.Instance.service_provider.localized_logger()

    @property
    def localization_manager(self) -> LocalizationManager:
        return BrowserServices.Instance.service_provider.localization_manager()
