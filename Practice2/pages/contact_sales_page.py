from playwright.sync_api import Page
from .base_page import BasePage


class ContactSalesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # 🔹 Поля формы
        self.first_name_input = page.get_by_label("First name")
        self.last_name_input = page.get_by_label("Last name")

    def fill_first_name(self, value: str):
        self.first_name_input.fill(value)

    def fill_last_name(self, value: str):
        self.last_name_input.fill(value)

    def assert_first_name_value(self, expected: str):
        assert self.first_name_input.input_value() == expected

    def assert_last_name_value(self, expected: str):
        assert self.last_name_input.input_value() == expected
