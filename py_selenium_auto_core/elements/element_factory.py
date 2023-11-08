from typing import Type, List, TypeVar

from selenium.webdriver.common.by import By

from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.elements.constants.elements_count import ElementsCount
from py_selenium_auto_core.elements.core_element import CoreElement
from py_selenium_auto_core.elements.element_finder import ElementFinder
from py_selenium_auto_core.localization.localization_manager import LocalizationManager
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto_core.waitings.conditional_wait import ConditionalWait


def _generate_xpath_locator(locator: Locator, index: int = None) -> Locator:
    """Generates xpath locator for target element"""

    if locator.by == By.ID:
        loc = f"//*[@id='{locator.value}']"
    elif locator.by == By.CLASS_NAME:
        loc = f"//*[@class='{locator.value}']"
    elif locator.by == By.NAME:
        loc = f"//*[@name='{locator.value}']"
    elif locator.by == By.TAG_NAME:
        loc = f"//{locator.value}"
    elif locator.by == By.XPATH:
        loc = locator.value
    else:
        raise ValueError(f"No such expected value: {locator.by}")

    if index is not None:
        return Locator(By.XPATH, f"({loc})[{index}]")
    return Locator(By.XPATH, loc)


def _generate_child_locator(parent_locator: Locator, child_locator: Locator):
    """Generates absolute child locator for target element"""

    par_loc = _generate_xpath_locator(parent_locator)
    if child_locator.by != By.XPATH:
        ch_loc_t = _generate_xpath_locator(child_locator).value
    else:
        if child_locator.value.startswith("./"):
            ch_loc_t = child_locator.value.split(".")[1]
        elif child_locator.value.startswith("/"):
            ch_loc_t = child_locator.value
        else:
            ch_loc_t = f"//child::{child_locator.value}"

    return Locator(By.XPATH, f"{par_loc.value}{ch_loc_t}")


T = TypeVar("T", bound=CoreElement, covariant=True)


class ElementFactory:
    """Factory that creates elements"""

    def __init__(
        self,
        conditional_wait: ConditionalWait,
        element_finder: ElementFinder,
        localization_manager: LocalizationManager,
    ):
        self._conditional_wait = conditional_wait
        self._element_finder = element_finder
        self._localization_manager = localization_manager

    @staticmethod
    def find_child_element(
        element_type: Type[T],
        parent_element: T,
        child_locator: Locator,
        name: str = None,
        state: ElementState = ElementState.Displayed,
    ):
        """Finds child element by its locator relative to parent element

        Args:
            element_type: Type of the element to create
            parent_element: Parent element
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
        return element_type(
            _generate_child_locator(parent_element.locator, child_locator),
            name or f"Child element of {parent_element.name}",
            state,
        )

    def find_child_elements(
        self,
        element_type: Type[T],
        parent_element: T,
        child_locator: Locator,
        name: str = None,
        expected_count: ElementsCount = ElementsCount.Any,
        state: ElementState = ElementState.Displayed,
    ) -> List[T]:
        """Finds list of child elements by their locator relative to parent element

        Args:
            element_type: Type of the element to create
            parent_element: Parent element
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
        return self.find_elements(
            element_type,
            _generate_child_locator(parent_element.locator, child_locator),
            name or f"Child element of {parent_element.name}",
            expected_count,
            state,
        )

    def find_elements(
        self,
        element_type: Type[T],
        locator: Locator,
        name: str = None,
        expected_count: ElementsCount = ElementsCount.Any,
        state: ElementState = ElementState.Displayed,
    ) -> List[T]:
        """Finds list of elements by base locator

        Args:
            element_type: Type of the element to create
            locator: Base elements locator
            name: Elements name
            expected_count: Expected number of elements that have to be found (zero, more then zero, any)
            state: Elements state

        Returns:
            List of child elements
        """
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
            elements.append(element_type(_generate_xpath_locator(locator, index), f"{name} + {index}", state))
        return elements

    @staticmethod
    def get_custom_element(
        element_type: Type[T],
        locator: Locator,
        name: str = None,
        state: ElementState = ElementState.Displayed,
    ):
        """Create custom element according to passed parameters

        Args:
            element_type: Type of the target element
            locator: Locator of the target element
            name: Name of the target element
            state: State of the target element

        Returns:
            Instance of custom element
        """
        return element_type(locator, name, state)
