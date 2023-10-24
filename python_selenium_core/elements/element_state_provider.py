import logging
from typing import Callable

from selenium.webdriver.remote.webelement import WebElement

from python_selenium_core.elements.constants.desired_state import DesiredState
from python_selenium_core.elements.constants.element_state import ElementState
from python_selenium_core.elements.element_finder import ElementFinder
from python_selenium_core.locator.locator import Locator
from python_selenium_core.waitings.conditional_wait import ConditionalWait


class ElementStateProvider:

    def __init__(
            self,
            locator: Locator,
            conditional_wait: ConditionalWait,
            element_finder: ElementFinder,
            log_element_state: Callable[[str, str], None]
    ):
        self.__locator = locator
        self.__conditional_wait = conditional_wait
        self.__element_finder = element_finder
        self.__log_element_state = log_element_state

    def is_displayed(self) -> bool:
        return self.wait_for_displayed(0)

    def is_exist(self) -> bool:
        return self.wait_for_exist(0)

    def is_enabled(self) -> bool:
        return self.wait_for_enabled(0)

    def is_clickable(self) -> bool:
        return self.__is_element_clickable(0, True)

    def wait_for_displayed(self, timeout: float = None) -> bool:
        def _predicate():
            return self.__is_any_element_found(timeout, ElementState.Displayed)
        return self.__do_and_log_wait_for_state(_predicate, "displayed", timeout)

    def wait_for_not_displayed(self, timeout: float = None) -> bool:
        def _predicate():
            return self.__conditional_wait.wait_for_condition(lambda: not self.is_displayed(), timeout)
        return self.__do_and_log_wait_for_state(_predicate, "not.displayed", timeout)

    def wait_for_exist(self, timeout: float = None) -> bool:
        def _predicate():
            return self.__is_any_element_found(timeout, ElementState.ExistsInAnyState)
        return self.__do_and_log_wait_for_state(_predicate, "exist", timeout)

    def wait_for_not_exist(self, timeout: float = None) -> bool:
        def _predicate():
            return self.__conditional_wait.wait_for_condition(lambda: not self.is_exist(), timeout)
        return self.__do_and_log_wait_for_state(_predicate, "not.exist", timeout)

    def wait_for_enabled(self, timeout: float = None) -> bool:
        def _predicate():
            return self.__is_element_in_desired_state(lambda e: self.__is_element_enabled(e), "ENABLED", timeout)
        return self.__do_and_log_wait_for_state(_predicate, "enabled", timeout)

    def wait_for_not_enabled(self, timeout: float = None) -> bool:
        def _predicate():
            return self.__is_element_in_desired_state(lambda e: not self.__is_element_enabled(e), "NOT ENABLED", timeout)
        return self.__do_and_log_wait_for_state(_predicate, "not.enabled", timeout)

    def wait_for_clickable(self, timeout: float = None):
        condition_key = "loc.el.state.clickable"
        try:
            self.__log_element_state("loc.wait.for.state", condition_key)
            self.__is_element_clickable(timeout, False)
        except:
            self.__log_element_state("loc.wait.for.state.failed", condition_key)
            raise

    def __is_element_clickable(self, timeout: float, catch_exception: bool) -> bool:
        desired_state = DesiredState(lambda element: element.is_displayed() and element.is_enabled(), "CLICKABLE")
        desired_state.is_catching_timeout_exception = catch_exception
        return self.__is_element_in_desired_condition(timeout, desired_state)

    def __is_element_in_desired_condition(self, timeout: float, element_state: DesiredState) -> bool:
        return any(self.__element_finder.find_elements(self.__locator, element_state, timeout))

    def __is_any_element_found(self, timeout: float, state: ElementState) -> bool:
        return any(self.__element_finder.find_elements(self.__locator, state, timeout))

    def __is_element_enabled(self, element: WebElement) -> bool:
        return element.is_enabled() and "disabled" not in element.get_attribute("class")

    def __is_element_in_desired_state(self, function: Callable[[WebElement], bool], state: str, timeout: float) -> bool:
        desired_state = DesiredState(function, state)
        desired_state.is_catching_timeout_exception = True
        desired_state.is_throwing_no_such_element_exception = True
        return self.__is_element_in_desired_condition(timeout, desired_state)

    def __do_and_log_wait_for_state(self, function: Callable[[], bool], msg_key: str, timeout: float = None) -> bool:
        if timeout is None or timeout == 0:
            return function()

        condition_key = f"loc.el.state.{msg_key}"
        self.__log_element_state("loc.wait.for.state", condition_key)
        result = self.__conditional_wait.wait_for_condition(function, timeout)
        if not result:
            self.__log_element_state("loc.wait.for.state.failed", condition_key)
        return result