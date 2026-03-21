from pages.login_page import LoginPage
import pytest

@pytest.mark.ui
@pytest.mark.smoke
def test_login_success(page, testsite_creds):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(testsite_creds["user"], testsite_creds["password"])

    assert login_page.is_logout_visible()
