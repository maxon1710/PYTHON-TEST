import pytest


pytest_plugins = (
    "fixtures.ui_fixtures",
    "fixtures.auth_fixtures",
    "fixtures.api_fixtures",
)


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Playwright in headless mode.",
    )
