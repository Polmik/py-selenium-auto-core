from typing import Type, List

import pytest
from selenium.webdriver.common.by import By

from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.elements.constants.elements_count import ElementsCount
from py_selenium_auto_core.elements.core_element import CoreElement
from py_selenium_auto_core.locator.locator import Locator
from tests.applications.browser.elements.label import Label
from tests.applications.browser.test_find_elements import BaseTestFindElements


class TestFindChildElements(BaseTestFindElements):
    __test__ = True

    custom_parent: Label = Label(
        Locator(By.XPATH, "//div[contains(@class,'figure')]"),
        "custom parent",
        ElementState.ExistsInAnyState,
    )

    hidden_elements_loc = Locator(By.XPATH, ".//h5")
    displayed_elements_loc = Locator(By.XPATH, ".//img[@alt='User Avatar']")
    not_exist_element_loc = Locator(By.XPATH, ".//div[@class='testtest']")

    @pytest.fixture(
        params=[
            Locator(By.XPATH, "//img"),
            Locator(By.XPATH, "img"),
            Locator(By.XPATH, ".//img"),
            Locator(By.TAG_NAME, "img"),
        ]
    )
    def supported_locator(self, request):
        return request.param

    def find_elements(
        self,
        element_type: Type[CoreElement],
        locator: Locator,
        name: str = None,
        expected_count=ElementsCount.Any,
        state: ElementState = ElementState.Displayed,
    ) -> List[CoreElement]:
        return self.parent_element.find_child_elements(element_type, locator, name, expected_count, state)

    def test_correct_number_of_children_for_relative_child_locator(self, supported_locator):
        exp_count = 3
        elements = self.element_factory.find_child_elements(Label, self.custom_parent, supported_locator)
        assert (
            len(elements) == exp_count
        ), f"Elements count for relative locator [{supported_locator}] should be {exp_count}"

    def test_set_workable_locators_to_child_elements(self, supported_locator):
        elements = self.element_factory.find_child_elements(Label, self.custom_parent, supported_locator)
        [el.get_element() for el in elements]

    def test_set_xpath_loc_in_find_child_element_if_both_parent_and_children(self, supported_locator):
        element = self.custom_parent.find_child_element(Label, supported_locator)
        self.check_child_locator_is_xpath_and_starts_from_parent(element.locator)

    def test_set_xpath_loc_in_find_child_elements_if_both_parent_and_children(self, supported_locator):
        elements = self.custom_parent.find_child_elements(Label, supported_locator)
        for el in elements:
            self.check_child_locator_is_xpath_and_starts_from_parent(el.locator)

    def check_child_locator_is_xpath_and_starts_from_parent(self, locator: Locator):
        assert locator.by == By.XPATH
        assert self.custom_parent.locator.value in locator.value
