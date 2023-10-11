from selenium.webdriver.common.by import By


class Locator:

    def __init__(self, by: By, value: str):
        self.by = by
        self.value = value

    def to_string(self):
        return f"By.{str(self.by).upper().replace(' ', '_')}: {self.value}"
