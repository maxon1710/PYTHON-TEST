from playwright.sync_api import expect

from config import urls
from .base_page import BasePage


class LoginPage(BasePage):
    url = urls.THE_INTERNET_LOGIN_URL

    # Playwright не использует By
    username_input = "input#username"
    password_input = "input#password"
    login_button = "button[type='submit']"
    logout_button = "a.button.secondary.radius"

    def login(self, username, password):
        self.page.fill(self.username_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

        # ожидание, что кнопка Logout видна
        expect(self.page.locator(self.logout_button)).to_be_visible()

    def is_logout_visible(self):
        return self.page.locator(self.logout_button).is_visible()
