from typing import Type, List, TypeVar

from selenium.webdriver.common.by import By

from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.elements.constants.elements_count import ElementsCount
from py_selenium_auto_core.elements.core_element import CoreElement
from py_selenium_auto_core.elements.element_finder import ElementFinder
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait

T = TypeVar("T", bound=CoreElement, covariant=True)


class ElementFactory:

    def __init__(
            self,
            conditional_wait: ConditionalWait,
            element_finder: ElementFinder,
            localization_manager: LocalizationManager
    ):
        self._conditional_wait = conditional_wait
        self._element_finder = element_finder
        self._localization_manager = localization_manager

    def find_child_element(self):
        pass

    def find_child_elements(self):
        pass

    def find_elements(
            self,
            element_type: Type[T],
            locator: Locator,
            name: str = None,
            expected_count: ElementsCount = ElementsCount.Any,
            state: ElementState = ElementState.Displayed
    ) -> List[T]:
        timeout = 0
        if expected_count == ElementsCount.Zero:
            self._conditional_wait.wait_for_true(
                function=lambda: not any(self._element_finder.find_elements(locator, state, timeout, name)),
                message=self._localization_manager.get_localized_message(
                    "loc.elements.with.name.found.but.should.not",
                    name,
                    locator.to_string(),
                    state.value,
                ),
            )
        elif expected_count == ElementsCount.MoreThenZero:
            self._conditional_wait.wait_for_true(
                function=lambda: any(self._element_finder.find_elements(locator, state, timeout, name)),
                message=self._localization_manager.get_localized_message(
                    "loc.no.elements.with.name.found.by.locator",
                    name,
                    locator.to_string(),
                ),
            )
        elif expected_count == ElementsCount.Any:
            self._conditional_wait.wait_for_condition(
                function=lambda: self._element_finder.find_elements(locator, state, timeout, name) is not None,
            )
        else:
            raise ValueError(f"No such expected value: {expected_count}")

        web_elements = self._element_finder.find_elements(locator, state, 0, name)
        elements = []
        name = "element" if name is None else name
        for index, web_element in enumerate(web_elements, 1):
            elements.append(
                element_type(self.generate_xpath_locator_by_index(locator, index), f"{name} + {index}", state))
        return elements

    def get_custom_element(self):
        pass

    def generate_locator(self):
        pass

    def generate_absolute_child_locator(self):
        pass

    def generate_xpath_locator(self, locator: Locator) -> Locator:
        if locator.by == By.ID:
            loc = f"//*[@id='{locator.value}']"
        elif locator.by == By.CLASS_NAME:
            loc = f"//*[@class='{locator.value}']"
        elif locator.by == By.NAME:
            loc = f"//*[@name='{locator.value}']"
        elif locator.by == By.XPATH:
            loc = locator.value
        else:
            raise ValueError(f"No such expected value: {locator.by}")

        return Locator(By.XPATH, loc)

    def generate_xpath_locator_by_index(self, locator: Locator, index: int) -> Locator:
        if locator.by == By.ID:
            loc = f"//*[@id='{locator.value}']"
        elif locator.by == By.CLASS_NAME:
            loc = f"//*[@class='{locator.value}']"
        elif locator.by == By.NAME:
            loc = f"//*[@name='{locator.value}']"
        elif locator.by == By.XPATH:
            loc = locator.value
        else:
            raise ValueError(f"No such expected value: {locator.by}")

        return Locator(By.XPATH, f"({loc})[{index}]")
