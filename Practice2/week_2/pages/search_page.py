from playwright.sync_api import Page


class SearchPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = page.locator("input[name='q']")

    def open(self):
        self.page.goto("https://duckduckgo.com/")

    def search(self, text: str):
        self.search_input.fill(text)
        self.search_input.press("Enter")
