from __future__ import annotations

from typing import Callable, Any, List

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from core.elements.constants.desired_state import DesiredState
from core.elements.constants.element_state import ElementState
from core.localization.localized_logger import LocalizedLogger
from core.locator.locator import Locator
from core.waitings.conditional_wait import ConditionalWait


class ElementFinder:

    def __init__(self, logger: LocalizedLogger, conditional_wait: ConditionalWait):
        self.__conditional_wait = conditional_wait
        self.__logger = logger

    def find_element(
            self,
            locator: Locator,
            state: ElementState | Callable[[WebElement], bool] = ElementState.ExistsInAnyState,
            state_name: str = "desired",
            timeout: float = None,
            name: str = None) -> WebElement:
        if isinstance(state, ElementState):
            desired_state = self._resolve_state(state)
            return self.find_element(
                locator=locator,
                state=desired_state.element_state_condition,
                state_name=desired_state.state_name,
                timeout=timeout,
                name=name
            )
        elif isinstance(state, Callable):
            return self.__find_element(
                locator=locator,
                state=state,
                state_name=state_name,
                timeout=timeout,
                name=name
            )

    def find_elements(
            self,
            locator: Locator,
            state: ElementState | DesiredState | Callable[[Any], bool] = ElementState.ExistsInAnyState,
            timeout: float = None,
            name: str = None
    ) -> List[WebElement]:
        if isinstance(state, ElementState):
            desired_state = self._resolve_state(state)
            desired_state.is_catching_timeout_exception = True
            return self.__find_elements(locator, desired_state, timeout, name)
        elif isinstance(state, DesiredState):
            return self.__find_elements(locator, state, timeout, name)
        elif isinstance(state, Callable):
            desired_state = DesiredState(state, "desired")
            desired_state.is_catching_timeout_exception = True
            return self.__find_elements(locator, desired_state, timeout, name)

    def _resolve_state(self, state: ElementState) -> DesiredState:
        if state.Displayed is ElementState.Displayed:
            def element_state_condition(element: WebElement) -> bool:
                return element.is_displayed()
        elif state.ExistsInAnyState is ElementState.ExistsInAnyState:
            def element_state_condition(element: WebElement) -> bool:
                return True
        else:
            raise NotImplementedError(f"{state} state is not recognized")
        return DesiredState(function_condition=element_state_condition, state_name=state.name)

    def __find_element(
            self,
            locator: Locator,
            state: Callable[[WebElement], bool],
            state_name: str,
            timeout: float,
            name: str
    ) -> WebElement:
        desired_state = DesiredState(state, state_name)
        desired_state.is_catching_timeout_exception = False
        desired_state.is_throwing_no_such_element_exception = True
        return self.__find_elements(locator=locator, state=desired_state, timeout=timeout, name=name)[0]

    def __find_elements(self, locator: Locator, state: Any, timeout, name) -> List[WebElement]:
        found_elements: List[WebElement] = []
        result_elements: List[WebElement] = []

        try:
            def predicate(driver: WebDriver) -> bool:
                found_elements.extend(driver.find_elements(by=locator.by, value=locator.value))
                result_elements.extend([el for el in found_elements if state.element_state_condition(el)])
                return any(result_elements)

            self.__conditional_wait.wait_for_driver(predicate, timeout)
        except TimeoutException as e:
            self.__handle_error(e, state, locator, found_elements, name)
        return result_elements

    def __handle_error(
            self,
            exception: TimeoutException,
            desired_state: DesiredState,
            locator: Locator,
            found_elements: list,
            name=None
    ) -> None:
        if name is None or name == "":
            message = f"No elements with locator '{locator.by}: {locator.value}' were found in {desired_state.state_name} state"
        else:
            message = f"Element [{name}] was not found by locator '{locator.by}: {locator.value}' in {desired_state.state_name} state"

        if desired_state.is_catching_timeout_exception:
            if not any(found_elements):
                if desired_state.is_throwing_no_such_element_exception:
                    raise NoSuchElementException(message)
                self.__logger.debug("loc.no.elements.found.in.state", None, locator.to_string(), desired_state.state_name)
            else:
                self.__logger.debug("loc.elements.were.found.but.not.in.state", None, locator.to_string(), desired_state.state_name)
        else:
            if desired_state.is_throwing_no_such_element_exception and not any(found_elements):
                raise NoSuchElementException(f"{message}: {exception.msg}")
            raise TimeoutException(f"{exception.msg}: {message}")
