from playwright.sync_api import Page
from .base_page import BasePage
from .solutions_menu import SolutionsMenu


class GitHubPublicHomePage(BasePage):
    url = "https://github.com/"

    def __init__(self, page: Page):
        super().__init__(page)

        # 🔹 Кнопка Solutions в хедере
        self.solutions_button = page.locator(
            'button:has-text("Solutions")'
        )

    def open(self):
        """
        Открываем публичную главную GitHub
        """
        super().open()

    def open_solutions_menu(self) -> SolutionsMenu:
        """
        Наводим мышь на Solutions и возвращаем объект меню
        """
        self.solutions_button.hover()
        return SolutionsMenu(self.page)
