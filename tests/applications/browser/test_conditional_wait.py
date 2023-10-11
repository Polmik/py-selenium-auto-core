from typing import Callable

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from core.locator.locator import Locator
from tests.applications.browser.browser_service import BrowserService
from tests.applications.browser.test_with_browser import TestWithBrowser
from core.waitings.conditional_wait import ConditionalWait


class TestConditionalWait(TestWithBrowser):

    wiki_url: str = "https://wikipedia.org"
    little_timeout = 1
    polling_interval = BrowserService.service_provider().timeout_configuration().polling_interval

    @pytest.fixture
    def conditional_wait(self) -> ConditionalWait:
        return BrowserService.service_provider().conditional_wait()

    @pytest.fixture
    def conditional_wait_for_condition(self, conditional_wait) -> Callable:
        return lambda condition, handled_exceptions: conditional_wait.wait_for_condition(
            condition,
            timeout=self.little_timeout,
            exceptions_to_ignore=handled_exceptions,
        )

    @pytest.fixture
    def conditional_wait_for_driver(self, conditional_wait) -> Callable:
        return lambda condition, handled_exceptions: conditional_wait.wait_for_driver(
            lambda driver: condition(),
            timeout=self.little_timeout,
            exceptions_to_ignore=handled_exceptions,
        )

    @pytest.fixture(name='conditional_wait_for_true')
    def conditional_wait_for_true(self, conditional_wait) -> Callable:
        return lambda condition, handled_exceptions: conditional_wait.wait_for_true(
            condition,
            timeout=self.little_timeout,
            exceptions_to_ignore=handled_exceptions,
        )

    @pytest.fixture(params=[
        "conditional_wait_for_condition",
        "conditional_wait_for_driver",
        "conditional_wait_for_true",
    ])
    def wait_with_handled_exception(self, request):
        return request.getfixturevalue(request.param)

    def test_should_be_possible_to_use_condition_with_driver(self, conditional_wait):
        def _predicate(driver: WebDriver):
            self.go_to_url(self.wiki_url, driver)
            return len(driver.find_elements(By.XPATH, "//*")) > 0
        conditional_wait.wait_for_driver(_predicate)

    def test_should_not_throw_on_wait_with_handled_exception(self, wait_with_handled_exception):
        index = [0]
        ex = AssertionError("Failure during conditional wait in handled exception")

        def predicate():
            index[0] += 1
            if index[0] == 2:
                return True
            raise ex

        wait_with_handled_exception(predicate, [AssertionError])

    def test_should_throw_on_wait_with_unhandled_exception(self, wait_with_handled_exception):
        index = [0]
        ex = AssertionError("Failure during conditional wait in handled exception")

        def predicate():
            index[0] += 1
            if index[0] == 2:
                return True
            raise ex

        try:
            wait_with_handled_exception(predicate, [NameError])
        except AssertionError:
            return

    def test_should_be_possible_to_use_conditional_wait_with_element_finder(self, conditional_wait):
        locator = Locator(By.XPATH, "//*[contains(., 'wikipedia')]")

        def element_finder_condition() -> bool:
            return len(self.service_provider.element_finder().find_elements(locator, timeout=self.little_timeout)) > 0

        def _predicate(driver: WebDriver):
            self.go_to_url(self.wiki_url, driver)
            return element_finder_condition()

        assert element_finder_condition() is False
        conditional_wait.wait_for_driver(_predicate)
