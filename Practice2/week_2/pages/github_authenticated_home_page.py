from playwright.sync_api import Page
from .base_page import BasePage


class GitHubAuthenticatedHomePage(BasePage):
    url = "https://github.com/"

    def __init__(self, page: Page):
        super().__init__(page)

        self.avatar = page.locator('img[data-testid="github-avatar"]')
        self.user_menu = page.locator(
            'div[role="dialog"][data-component="AnchoredOverlay"]'
        )

    def is_logged_in(self):
        self.avatar.wait_for(state="visible", timeout=7000)
        print("AVATAR VISIBLE:", self.avatar.is_visible())
        return self.avatar.is_visible()

    def open_user_menu(self):
        self.avatar.click()
        self.user_menu.wait_for(state="visible", timeout=7000)
