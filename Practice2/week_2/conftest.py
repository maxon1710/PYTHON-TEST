import os
import pytest
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    base_dir = os.path.dirname(os.path.dirname(__file__))  # Practice2
    env_path = os.path.join(base_dir, ".env")
    load_dotenv(env_path)



@pytest.fixture(scope="session")
def github_creds():
    user = os.getenv("GH_USER")
    password = os.getenv("GH_PASS")

    if not user or not password:
        pytest.skip("GH_USER/GH_PASS not set in .env")

    return {"user": user, "password": password}


@pytest.fixture(scope="session")
def testsite_creds():
    user = os.getenv("TEST_USER")
    password = os.getenv("TEST_PASS")

    if not user or not password:
        pytest.skip("TEST_USER/TEST_PASS not set in .env")

    return {"user": user, "password": password}


@pytest.fixture(scope="function")
def page(request):
    with sync_playwright() as p:
        cli_headless = request.config.getoption("--headless")
        env_headless = os.getenv("HEADLESS", "false").lower() == "true"
        headless = cli_headless or env_headless

        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        yield page
        browser.close()


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Playwright in headless mode.",
    )
