from __future__ import annotations

from typing import Callable, Any, List

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from py_selenium_auto_core.elements.constants.desired_state import DesiredState
from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.localization.localized_logger import LocalizedLogger
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait


class ElementFinder:
    """Provides ability to find elements in desired ElementState"""

    def __init__(self, logger: LocalizedLogger, conditional_wait: ConditionalWait):
        self._conditional_wait = conditional_wait
        self._logger = logger

    def find_element(
        self,
        locator: Locator,
        state: ElementState | Callable[[WebElement], bool] = ElementState.ExistsInAnyState,
        state_name: str = "desired",
        timeout: float = None,
        name: str = None,
    ) -> WebElement:
        """Finds element

        Args:
            locator: Element locator
            state: Desired ElementState or predicate to define element state
            state_name: Predicate to define element state
            timeout: Timeout for search
            name: Element name to be used for logging and exception message

        Returns:
            Found element

        Exception:
            NoSuchElementException: Thrown if element was not found in time in desired state
        """
        if isinstance(state, ElementState):
            # Convert ElementState to DesiredState and call this method again (Move to Callable section)
            desired_state = self._resolve_state(state)
            return self.find_element(
                locator=locator,
                state=desired_state.element_state_condition,
                state_name=desired_state.state_name,
                timeout=timeout,
                name=name,
            )
        elif isinstance(state, Callable):
            desired_state = DesiredState(state, state_name)
            desired_state.is_catching_timeout_exception = False
            desired_state.is_throwing_no_such_element_exception = True
            return self._find_elements(locator=locator, state=desired_state, timeout=timeout, name=name)[0]

        raise ValueError("Incorrect type of state")

    def find_elements(
        self,
        locator: Locator,
        state: ElementState | DesiredState | Callable[[Any], bool] = ElementState.ExistsInAnyState,
        timeout: float = None,
        name: str = None,
    ) -> List[WebElement]:
        """Finds elements

        Args:
            locator: Elements locator
            state: Desired ElementState or predicate to define element state
            timeout: Timeout for search
            name: Element name to be used for logging and exception message

        Returns:
            List of found elements
        """
        if isinstance(state, ElementState):
            # Convert ElementState to DesiredState and call this method again (Move to DesiredState section)
            desired_state = self._resolve_state(state)
            desired_state.is_catching_timeout_exception = True
            return self.find_elements(locator, desired_state, timeout, name)
        elif isinstance(state, Callable):
            # Convert Callable to DesiredState and call this method again (Move to DesiredState section)
            desired_state = DesiredState(state, "desired")
            desired_state.is_catching_timeout_exception = True
            return self.find_elements(locator, desired_state, timeout, name)
        elif isinstance(state, DesiredState):
            return self._find_elements(locator, state, timeout, name)
        raise ValueError("Incorrect type of state")

    def _resolve_state(self, state: ElementState) -> DesiredState:
        if state == ElementState.Displayed:

            def element_state_condition(element: WebElement) -> bool:
                return element.is_displayed()

        elif state == ElementState.ExistsInAnyState:

            def element_state_condition(element: WebElement) -> bool:
                return True

        else:
            raise ValueError(f"{state} state is not recognized")
        return DesiredState(function_condition=element_state_condition, state_name=state.name)

    def _find_elements(self, locator: Locator, state: DesiredState, timeout, name) -> List[WebElement]:
        found_elements: List[WebElement] = []
        result_elements: List[WebElement] = []

        try:

            def predicate(driver: WebDriver) -> bool:
                found_elements.extend(driver.find_elements(by=locator.by, value=locator.value))
                result_elements.extend([el for el in found_elements if state.element_state_condition(el)])
                return any(result_elements)

            self._conditional_wait.wait_for_driver(predicate, timeout)
        except TimeoutException as e:
            self._handle_timeout_exception(e, state, locator, found_elements, name)
        return result_elements

    def _handle_timeout_exception(
        self,
        exception: TimeoutException,
        desired_state: DesiredState,
        locator: Locator,
        found_elements: list,
        name=None,
    ) -> None:
        if name is None or name == "":
            message = (
                f"No elements with locator '{locator.by}: {locator.value}'"
                f" were found in {desired_state.state_name} state"
            )
        else:
            message = (
                f"Element [{name}] was not found by locator"
                f" '{locator.by}: {locator.value}' in {desired_state.state_name} state"
            )

        if desired_state.is_catching_timeout_exception:
            if not any(found_elements):
                if desired_state.is_throwing_no_such_element_exception:
                    raise NoSuchElementException(message)
                self._logger.debug(
                    "loc.no.elements.found.in.state",
                    None,
                    locator.to_string(),
                    desired_state.state_name,
                )
            else:
                self._logger.debug(
                    "loc.elements.were.found.but.not.in.state",
                    None,
                    locator.to_string(),
                    desired_state.state_name,
                )
        else:
            if desired_state.is_throwing_no_such_element_exception and not any(found_elements):
                raise NoSuchElementException(f"{message}: {exception.msg}")
            raise TimeoutException(f"{exception.msg}: {message}")
