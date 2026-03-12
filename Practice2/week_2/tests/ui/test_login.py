from ...pages.login_page import LoginPage
import pytest

@pytest.mark.ui
@pytest.mark.smoke

def test_login_success(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("tomsmith", "SuperSecretPassword!")

    assert login_page.is_logout_visible()
