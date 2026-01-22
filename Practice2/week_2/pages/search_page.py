from selenium.webdriver.common.by import By


class SearchPage:
    SEARCH_INPUT = (By.NAME, "q")

    def __init__(self, browser):
        self.browser = browser

    def open(self):
        self.browser.get("https://duckduckgo.com/")

    def search(self, text):
        search_input = self.browser.find_element(*self.SEARCH_INPUT)
        search_input.send_keys(text)
        search_input.submit()
