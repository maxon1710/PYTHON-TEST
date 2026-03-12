from playwright.sync_api import Page

from config import urls


class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.locator("input[name='q']")

    def open(self):
        self.page.goto(urls.DUCKDUCKGO_URL)

    def search(self, text: str):
        self.search_input.fill(text)
        self.search_input.press("Enter")
