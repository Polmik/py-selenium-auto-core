from selenium.webdriver.common.by import By


class Locator:
    """Wrapper for Selenium Locator"""

    def __init__(self, by: By, value: str):
        """

        Args:
            by: Supported locator strategies
            value: Selector

        Example:
            Locator(By.ID, 'close')
        """
        self.by = by
        self.value = value

    def to_string(self):
        return f"By.{str(self.by).upper().replace(' ', '_')}: {self.value}"

    def __repr__(self):
        return self.to_string()
