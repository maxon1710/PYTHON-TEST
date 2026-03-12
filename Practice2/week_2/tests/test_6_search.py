import pytest
from week_2.pages.six_search import SixSearch


@pytest.mark.parametrize("query", ["qa", "aqa", "cars"])
def test_six_search(page, query):
    six_search = SixSearch(page)

    six_search.open()
    six_search.search(query)

    assert "q=" in page.url