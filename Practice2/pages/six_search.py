from playwright.sync_api import Page

from config import urls


class SixSearch:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.locator("input[name='q']")

        # более стабильный селектор результатов
        self.organic_results = page.locator("article")

    def open(self):
        self.page.goto(urls.DUCKDUCKGO_URL)

    def search(self, text: str):
        self.search_input.click()
        self.search_input.fill(text)
        self.search_input.press("Enter")

    def sixth_result(self):
        return self.organic_results.nth(5)