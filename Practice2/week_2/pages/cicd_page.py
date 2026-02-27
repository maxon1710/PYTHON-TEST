from playwright.sync_api import Page
from .base_page import BasePage


class CiCdPage(BasePage):
    url = "https://github.com/solutions/use-case/ci-cd"

    def __init__(self, page: Page):
        super().__init__(page)

        self.contact_sales_button = page.locator(
            'a[href*="enterprise/contact"][href*="ref_loc=hero"]'
        )

    def is_opened(self) -> bool:
        """
        Проверяем, что мы на странице CI/CD
        """
        return "/solutions/use-case/ci-cd" in self.page.url

    def click_contact_sales(self):
        """
        Переходим на страницу Contact Sales
        """
        self.contact_sales_button.wait_for(state="visible", timeout=7000)
        self.contact_sales_button.click()
