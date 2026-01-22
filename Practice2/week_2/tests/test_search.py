from week_2.pages.search_page import SearchPage

def test_simple_search(browser):
    page = SearchPage(browser)
    page.open()
    page.search("pytest selenium")

    assert "pytest" in browser.title.lower()
