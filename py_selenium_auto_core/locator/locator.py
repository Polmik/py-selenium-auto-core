from dataclasses import dataclass

from selenium.webdriver.common.by import By


@dataclass
class Locator:
    """Wrapper for Selenium Locator"""

    by: By
    value: str

    def to_string(self):
        return f"By.{str(self.by).upper().replace(' ', '_')}: {self.value}"

    @staticmethod
    def by_xpath(value: str) -> "Locator":
        return Locator(By.XPATH, value)

    @staticmethod
    def by_id(value: str) -> "Locator":
        return Locator(By.ID, value)

    @staticmethod
    def by_class_name(value: str) -> "Locator":
        return Locator(By.CLASS_NAME, value)

    @staticmethod
    def by_tag_name(value: str) -> "Locator":
        return Locator(By.TAG_NAME, value)

    @staticmethod
    def by_name(value: str) -> "Locator":
        return Locator(By.NAME, value)

    @staticmethod
    def by_css_selector(value: str) -> "Locator":
        return Locator(By.CSS_SELECTOR, value)

    @staticmethod
    def by_link_text(value: str) -> "Locator":
        return Locator(By.LINK_TEXT, value)

    @staticmethod
    def by_partial_link_text(value: str) -> "Locator":
        return Locator(By.PARTIAL_LINK_TEXT, value)

    def __repr__(self):
        return self.to_string()
