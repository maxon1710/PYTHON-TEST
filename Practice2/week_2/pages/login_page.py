from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from week_2.pages.base_page import BasePage


class LoginPage(BasePage):

    url = "https://the-internet.herokuapp.com/login"

    username_input = (By.ID, "username")
    password_input = (By.ID, "password")
    login_button = (By.CSS_SELECTOR, "button[type='submit']")
    logout_button = (By.CSS_SELECTOR, "a.button.secondary.radius")

    def open(self):
        self.browser.get(self.url)

    def login(self, username, password):
        self.browser.find_element(*self.username_input).send_keys(username)
        self.browser.find_element(*self.password_input).send_keys(password)
        self.browser.find_element(*self.login_button).click()

        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(self.logout_button)
        )

    def is_logout_visible(self):
        return self.browser.find_element(*self.logout_button).is_displayed()