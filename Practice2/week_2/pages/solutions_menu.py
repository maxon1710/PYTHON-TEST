from playwright.sync_api import Page


class SolutionsMenu:
    def __init__(self, page: Page):
        self.page = page

        # 🔹 Пункт CI/CD внутри выпадающего меню
        self.cicd_link = page.locator(
            'a[href="https://github.com/solutions/use-case/ci-cd"]'
        )

    def click_ci_cd(self):
        """
        Кликаем по пункту CI/CD
        """
        self.cicd_link.wait_for(state="visible", timeout=7000)
        self.cicd_link.click()
