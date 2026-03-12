from playwright.sync_api import Page

from config import urls
from config.settings import UI_TIMEOUT_MS
from .base_page import BasePage


class GitHubLoginPage(BasePage):
    url = urls.GITHUB_LOGIN_URL

    def __init__(self, page: Page):
        super().__init__(page)

        # 🔹 локатор контейнера ошибки логина
        # появляется при неуспешной авторизации
        self.error_alert = page.locator(
            'div[role="alert"].js-flash-alert'
        )

    def login(self, username: str, password: str):
        """
        Ввод логина и пароля + нажатие Sign in
        """
        self.page.fill('input[name="login"]', username)
        self.page.fill('input[name="password"]', password)

        # 🔥 ВАЖНО: именно здесь мы НАЖИМАЕМ Sign in
        self.page.click('input[type="submit"][value="Sign in"]')

    def wait_for_login_error(self, timeout: int = UI_TIMEOUT_MS):
        """
        Ждём появления ошибки логина.
        Защита от flaky-тестов.
        """
        self.error_alert.wait_for(state="visible", timeout=timeout)

    def get_login_error_text(self) -> str:
        """
        Возвращает текст ошибки логина.
        Переносы строк и пробелы нас не волнуют.
        """
        return self.error_alert.inner_text()

    def is_login_error_contains(self, expected_text: str) -> bool:
        """
        Проверяем, что текст ошибки содержит ожидаемую строку.
        Используем contains, а не equals — защита от вёрстки.
        """
        self.wait_for_login_error()
        return expected_text in self.get_login_error_text()
