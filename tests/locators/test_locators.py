from typing import Callable

import pytest
from selenium.webdriver.common.by import By

from py_selenium_auto_core.locator.locator import Locator


class TestLocators:
    @pytest.mark.parametrize(
        argnames=("method", "by"),
        argvalues=[
            pytest.param(Locator.by_xpath, By.XPATH),
            pytest.param(Locator.by_id, By.ID),
            pytest.param(Locator.by_class_name, By.CLASS_NAME),
            pytest.param(Locator.by_tag_name, By.TAG_NAME),
            pytest.param(Locator.by_name, By.NAME),
            pytest.param(Locator.by_css_selector, By.CSS_SELECTOR),
            pytest.param(Locator.by_link_text, By.LINK_TEXT),
            pytest.param(Locator.by_partial_link_text, By.PARTIAL_LINK_TEXT),
        ],
    )
    def test_generate_locator(self, method: Callable, by: By):
        selector = "temp"
        assert method(selector) == Locator(by, selector)
