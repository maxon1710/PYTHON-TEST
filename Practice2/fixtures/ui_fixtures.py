# ui_fixtures.py
import pytest
import allure
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

        # После теста — проверяем упал ли и делаем скриншот
        rep = getattr(request.node, "rep_call", None)
        if rep and rep.failed:
            allure.attach(
                page.screenshot(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                page.content(),
                name="page_html",
                attachment_type=allure.attachment_type.HTML
            )

        browser.close()