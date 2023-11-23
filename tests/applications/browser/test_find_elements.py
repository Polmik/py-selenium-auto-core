import pytest
from dependency_injector.providers import Singleton
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from typing import Type, List

from py_selenium_auto_core.configurations.timeout_configuration import TimeoutConfiguration
from tests.applications.browser.test_with_browser import TestWithBrowser
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.elements.constants.elements_count import ElementsCount
from py_selenium_auto_core.elements.core_element import CoreElement
from py_selenium_auto_core.elements.element_factory import ElementFactory
from tests.applications.browser.browser_services import BrowserServices
from tests.applications.browser.elements.label import Label


class CustomTimeout(TimeoutConfiguration):
    def __init__(self):
        super().__init__({"timeouts": {}})

    @property
    def implicit(self) -> float:
        return 0

    @property
    def condition(self) -> float:
        return 3

    @property
    def polling_interval(self) -> float:
        return 0.3


class BaseTestFindElements(TestWithBrowser):
    __test__ = False

    content_loc: Locator = Locator(By.XPATH, "//div[contains(@class,'example')]")
    hovers_url: str = f"{TestWithBrowser.test_site}/hovers"
    hidden_elements_loc = Locator(By.XPATH, "//h5")
    displayed_elements_loc = Locator(By.XPATH, "//img[@alt='User Avatar']")
    dotted_loc = Locator(By.XPATH, "//img[@alt='User Avatar']/parent::div")
    not_exist_element_loc = Locator(By.XPATH, "//div[@class='testtest']")

    def find_elements(
        self,
        element_type: Type[CoreElement],
        locator: Locator,
        name: str = None,
        expected_count=ElementsCount.Any,
        state: ElementState = ElementState.Displayed,
    ) -> List[CoreElement]:
        return self.element_factory.find_elements(element_type, locator, name, expected_count, state)

    @pytest.fixture
    def reset_config(self, request):
        BrowserServices.Instance.service_provider.timeout_configuration.override(Singleton(CustomTimeout))
        request.addfinalizer(lambda: BrowserServices.Instance.service_provider.reset_override())
        yield

    @property
    def element_factory(self) -> ElementFactory:
        return BrowserServices.Instance.service_provider.element_factory()

    @property
    def parent_element(self) -> Label:
        return Label(self.content_loc, "Example", ElementState.ExistsInAnyState)

    def setup_method(self):
        super().setup_method()
        self.go_to_url(self.hovers_url)
        self.parent_element.click()

    @pytest.mark.parametrize(
        argnames=("count", "state", "expected_count"),
        argvalues=(
            pytest.param(ElementsCount.MoreThenZero, ElementState.Displayed, 3),
            pytest.param(ElementsCount.MoreThenZero, ElementState.ExistsInAnyState, 3),
            pytest.param(ElementsCount.Any, ElementState.Displayed, 3),
            pytest.param(ElementsCount.Any, ElementState.ExistsInAnyState, 3),
        ),
    )
    def test_find_elements_for_displayed_elements(
        self,
        count: ElementsCount,
        state: ElementState,
        expected_count: int,
    ):
        elements_count = len(self.find_elements(Label, self.displayed_elements_loc, expected_count=count, state=state))
        assert elements_count == expected_count, f"Elements count for hidden elements should be {elements_count}"

    @pytest.mark.parametrize(
        argnames=("count", "state", "expected_count"),
        argvalues=(
            pytest.param(ElementsCount.Zero, ElementState.Displayed, 0),
            pytest.param(ElementsCount.MoreThenZero, ElementState.ExistsInAnyState, 3),
            pytest.param(ElementsCount.Any, ElementState.Displayed, 0),
            pytest.param(ElementsCount.Any, ElementState.ExistsInAnyState, 3),
        ),
    )
    def test_find_elements_for_hidden_elements(
        self,
        count: ElementsCount,
        state: ElementState,
        expected_count: int,
    ):
        elements_count = len(self.find_elements(Label, self.hidden_elements_loc, expected_count=count, state=state))
        assert elements_count == expected_count, f"Elements count for hidden elements should be {elements_count}"

    @pytest.mark.parametrize(
        argnames=("count", "state", "expected_count"),
        argvalues=(
            pytest.param(ElementsCount.Zero, ElementState.Displayed, 0),
            pytest.param(ElementsCount.Zero, ElementState.ExistsInAnyState, 0),
            pytest.param(ElementsCount.Any, ElementState.Displayed, 0),
            pytest.param(ElementsCount.Any, ElementState.ExistsInAnyState, 0),
        ),
    )
    def test_find_elements_for_not_exists_elements(
        self,
        count: ElementsCount,
        state: ElementState,
        expected_count: int,
    ):
        elements_count = len(self.find_elements(Label, self.not_exist_element_loc, expected_count=count, state=state))
        assert elements_count == expected_count, f"Elements count for not existing elements should be {elements_count}"

    @pytest.mark.parametrize(
        argnames=("count", "state"),
        argvalues=(
            pytest.param(ElementsCount.Zero, ElementState.Displayed),
            pytest.param(ElementsCount.Zero, ElementState.ExistsInAnyState),
        ),
    )
    def test_impossible_to_find_displayed_elements_with_wrong_arguments(
        self,
        reset_config,
        count: ElementsCount,
        state: ElementState,
    ):
        try:
            self.find_elements(Label, self.displayed_elements_loc, expected_count=count, state=state)
        except TimeoutException:
            ...
        else:
            pytest.fail(f"Tried to find elements with expected count '{count}' and state '{state}'")

    @pytest.mark.parametrize(
        argnames=("count", "state"),
        argvalues=[
            pytest.param(ElementsCount.MoreThenZero, ElementState.Displayed),
            pytest.param(ElementsCount.Zero, ElementState.ExistsInAnyState),
        ],
    )
    def test_impossible_to_find_hidden_elements_with_wrong_arguments(
        self, reset_config, count: ElementsCount, state: ElementState
    ):
        is_error = False
        error_message = ""
        name = "custom name"
        try:
            self.find_elements(Label, self.hidden_elements_loc, name, expected_count=count, state=state)
        except TimeoutException as e:
            is_error = True
            error_message = str(e)
        assert is_error, f"Tried to find elements with expected count '{count}' and state '{state}'"
        assert name in error_message, f"Error message should contain element name: '{name}'"

    @pytest.mark.parametrize(
        argnames=("count", "state"),
        argvalues=(
            pytest.param(ElementsCount.MoreThenZero, ElementState.Displayed),
            pytest.param(ElementsCount.MoreThenZero, ElementState.ExistsInAnyState),
        ),
    )
    def test_impossible_to_find_not_exists_elements_with_wrong_arguments(
        self,
        reset_config,
        count: ElementsCount,
        state: ElementState,
    ):
        is_error = False
        try:
            self.find_elements(Label, self.not_exist_element_loc, expected_count=count, state=state)
        except TimeoutException:
            is_error = True
        assert is_error, f"Tried to find elements with expected count '{count}' and state '{state}'"

    def test_work_with_elements_found_by_dotted_locator(self):
        found_elements = self.find_elements(Label, self.dotted_loc, expected_count=ElementsCount.MoreThenZero)
        [e.get_element() for e in found_elements]


class TestFindElements(BaseTestFindElements):
    __test__ = True
