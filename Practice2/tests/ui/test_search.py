from pages.search_page import SearchPage
import pytest

@pytest.mark.ui
@pytest.mark.smoke
def test_simple_search(page):
    search_page = SearchPage(page)
    search_page.open()
    search_page.search("pytest selenium")

    assert "pytest" in page.title().lower()
