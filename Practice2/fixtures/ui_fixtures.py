import pytest
from playwright.sync_api import sync_playwright

from config.settings import HEADLESS


@pytest.fixture(scope="function")
def page(request):
    cli_headless = request.config.getoption("--headless")
    headless = cli_headless or HEADLESS

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        yield page
        browser.close()
