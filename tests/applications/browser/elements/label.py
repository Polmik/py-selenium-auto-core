from tests.applications.browser.elements.web_element import WebElement
from py_selenium_auto_core.elements.constants.element_state import ElementState
from py_selenium_auto_core.locator.locator import Locator


class Label(WebElement):
    def __init__(self, locator: Locator, name: str, element_state: ElementState):
        super().__init__(locator, name, element_state)

    @property
    def element_type(self) -> str:
        return "Label"
