import pytest
import allure

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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def attach_on_failure(request):
    yield

    rep = getattr(request.node, "rep_call", None)
    if not rep or not rep.failed:
        return

    page = request.node.funcargs.get("page")

    if page is not None:
        # UI тест
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
    else:
        # API тест
        allure.attach(
            str(rep.longrepr),
            name="failure_details",
            attachment_type=allure.attachment_type.TEXT
        )