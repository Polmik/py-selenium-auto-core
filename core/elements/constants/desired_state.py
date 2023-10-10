from typing import Callable


class DesiredState:
    is_catching_timeout_exception: bool = False
    is_throwing_no_such_element_exception: bool = False

    def __init__(self, function_condition: Callable, state_name: str):
        self.element_state_condition = function_condition
        self.state_name: str = state_name
