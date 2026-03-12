from playwright.sync_api import Page

from config import urls
from config.settings import UI_TIMEOUT_MS


class SolutionsMenu:
    def __init__(self, page: Page):
        self.page = page

        # 🔹 Пункт CI/CD внутри выпадающего меню
        self.cicd_link = page.locator(
            f'a[href="{urls.GITHUB_CICD_URL}"]'
        )

    def click_ci_cd(self):
        """
        Кликаем по пункту CI/CD
        """
        self.cicd_link.wait_for(state="visible", timeout=UI_TIMEOUT_MS)
        self.cicd_link.click()
