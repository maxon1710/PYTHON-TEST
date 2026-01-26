from playwright.sync_api import Page


class BasePage:
    url: str = ""

    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str | None = None):
        target_url = url or self.url
        self.page.goto(target_url)



