from week_2.pages.github_public_home_page import GitHubPublicHomePage
from week_2.pages.cicd_page import CiCdPage
from week_2.pages.contact_sales_page import ContactSalesPage
import pytest

@pytest.mark.regression
@pytest.mark.ui
def test_solutions_cicd_contact_sales_form(page):
    # --- GIVEN ---
    home_page = GitHubPublicHomePage(page)
    home_page.open()

    # --- WHEN ---
    solutions_menu = home_page.open_solutions_menu()
    solutions_menu.click_ci_cd()

    cicd_page = CiCdPage(page)
    assert cicd_page.is_opened(), "CI/CD page was not opened"

    cicd_page.click_contact_sales()

    # --- THEN ---
    contact_sales_page = ContactSalesPage(page)

    first_name = "Max"
    last_name = "Boytsov"

    contact_sales_page.fill_first_name(first_name)
    contact_sales_page.fill_last_name(last_name)

    contact_sales_page.assert_first_name_value(first_name)
    contact_sales_page.assert_last_name_value(last_name)
