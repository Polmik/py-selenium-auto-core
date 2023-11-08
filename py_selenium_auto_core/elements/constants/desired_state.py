from typing import Callable

from selenium.webdriver.remote.webelement import WebElement


class DesiredState:
    """Defines desired state for element with ability to handle exceptions"""

    def __init__(self, function_condition: Callable[[WebElement], bool], state_name: str):
        self.element_state_condition: Callable[[WebElement], bool] = function_condition
        self.state_name: str = state_name
        self.is_catching_timeout_exception: bool = False
        self.is_throwing_no_such_element_exception: bool = False
