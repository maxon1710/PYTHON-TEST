from week_2.pages.github_login_page import GitHubLoginPage
from week_2.pages.github_authenticated_home_page import GitHubAuthenticatedHomePage
import pytest

@pytest.mark.ui
@pytest.mark.external
def test_github_login_success(page, github_creds):
    login_page = GitHubLoginPage(page)
    authenticated_home_page = GitHubAuthenticatedHomePage(page)

    login_page.open()
    login_page.login(
        github_creds["user"],
        github_creds["password"]
    )

    assert authenticated_home_page.is_logged_in()
