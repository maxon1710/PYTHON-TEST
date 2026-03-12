from playwright.sync_api import Page

from config import urls
from .base_page import BasePage
from .resources_menu import ResourcesMenu
from .solutions_menu import SolutionsMenu


class GitHubPublicHomePage(BasePage):
    url = urls.GITHUB_BASE_URL

    def __init__(self, page: Page):
        super().__init__(page)

        # 🔹 Кнопка Solutions в хедере
        self.solutions_button = page.locator(
            'button:has-text("Solutions")'
        )

        # Кнопка Resources в хедере
        self.resources_button = page.locator(
            'button:has-text("Resources")'
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

    def open_resources_menu(self):
        """
        Наводим мышь на Resources и возвращаем объект меню
        """
        self.resources_button.hover()
        return ResourcesMenu(self.page)