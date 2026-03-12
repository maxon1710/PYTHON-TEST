import pytest
from ...pages.six_search import SixSearch
import pytest

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.parametrize("query", ["qa", "aqa", "cars"])
def test_six_search(page, query):
    six_search = SixSearch(page)

    six_search.open()
    six_search.search(query)

    assert "q=" in page.url
