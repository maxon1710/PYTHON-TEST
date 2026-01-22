import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--start-maximized")

    # ❗️ вот это отключает плашку сохранения пароля
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2
    })

    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()
