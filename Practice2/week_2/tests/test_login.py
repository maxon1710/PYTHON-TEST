from week_2.pages.login_page import LoginPage


def test_login_success(browser):
    page = LoginPage(browser)
    page.open()
    page.login("tomsmith", "SuperSecretPassword!")

    assert page.is_logout_visible()
