from week_2.pages.github_about_page import AboutPage


def test_careers(page):
    about_page = AboutPage(page)
    about_page.open()

    assert about_page.is_opened() is True

    about_page.click_careers()

    heading = page.locator('h1[token-data="LP.SKU-A1.HEADER"]')
    heading.wait_for(state="visible", timeout=20000)

    assert "github.careers" in page.url
    assert heading.is_visible()