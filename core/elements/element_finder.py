from __future__ import annotations

from typing import Callable, Any

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from core.elements.constants.desired_state import DesiredState
from core.elements.constants.element_state import ElementState
from core.locator.locator import Locator
from core.waitings.conditional_wait import ConditionalWait


class ElementFinder:

    def __init__(self, conditional_wait: ConditionalWait):
        self.__conditional_wait = conditional_wait

    def find_element(
            self,
            locator: Locator,
            state: ElementState | Callable = ElementState.ExistsInAnyState,
            state_name: str = "desired",
            timeout: int = None,
            name: str = None):
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
    ):
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

    def __find_element(self, locator: Locator, state: ElementState | Callable, state_name: str, timeout: int,
                       name: str):
        desired_state = DesiredState(state, state_name)
        desired_state.is_catching_timeout_exception = False
        desired_state.is_throwing_no_such_element_exception = True
        return self.__find_elements(locator=locator, state=desired_state, timeout=timeout, name=name)[0]

    def __find_elements(self, locator: Locator, state: Any, timeout, name) -> list:
        found_elements = []
        result_elements = []

        try:
            def condition(driver: WebDriver) -> bool:
                found_elements.extend(driver.find_elements(by=locator.by, value=locator.value))
                result_elements.extend([e for e in found_elements if state.element_state_condition(e)])
                return any(result_elements)

            self.__conditional_wait.wait_for_driver(condition, timeout)
        except TimeoutException as e:
            self.__handle_error(e, state, locator, found_elements, name)
        return result_elements


    def __handle_error(self, exception: TimeoutException, desired_state: DesiredState, locator: Locator, found_elements: list, name=None):
        message = f"Element [{name}] was not found by locator '{locator.by}: {locator.value}' in {desired_state.state_name} state"
        if name is not None or name == "":
            message = f"No elements with locator '{locator.by}: {locator.value}' were found in {desired_state.state_name} state"
        if desired_state.is_catching_timeout_exception:
            if not any(found_elements):
                if desired_state.is_throwing_no_such_element_exception:
                    raise NoSuchElementException(message)
                # TODO Log
            else:
                # TODO Log
                pass
        else:
            if desired_state.is_throwing_no_such_element_exception and not any(found_elements):
                raise NoSuchElementException(f"{message}: {exception.msg}")
            raise TimeoutException(f"{exception.msg}: {message}")