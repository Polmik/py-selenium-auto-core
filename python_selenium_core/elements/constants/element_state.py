import enum


class ElementState(enum.Enum):
    """Possible states of element"""

    Displayed = enum.auto()
    ExistsInAnyState = enum.auto()
