import random
import string
import pytest
from week_2.pages.github_login_page import GitHubLoginPage

# NOTE:
# Негативный тест использует случайный username.
# GitHub применяет anti-bot эвристики, возможна нестабильность теста.

@pytest.mark.regression
@pytest.mark.ui
def generate_random_username(length: int = 14) -> str:
    """
    Генерирует случайный username из букв и цифр.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def test_github_login_negative_random_user(page):
    login_page = GitHubLoginPage(page)

    random_username = generate_random_username()
    wrong_password = "WrongPassword123!"

    login_page.open()
    login_page.login(random_username, wrong_password)

    assert login_page.is_login_error_contains(
        "Incorrect username or password."
    )
