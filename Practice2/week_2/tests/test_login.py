from week_2.pages.login_page import LoginPage


def test_login_success(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("tomsmith", "SuperSecretPassword!")

    assert login_page.is_logout_visible()
