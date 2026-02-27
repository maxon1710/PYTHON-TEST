import pytest
from playwright.sync_api import expect
from week_2.pages.six_search import SixSearch

@pytest.mark.parametrize("query", ["qa", "aqa", "cars"])
def test_six_search(page, query):
    six_search = SixSearch(page)

    six_search.open()
    six_search.search(query)

    # 1️⃣ ЖДЁМ, что элементов минимум 6
    expect(six_search.organic_results.nth(5)).to_be_visible()

    # 2️⃣ ТЕПЕРЬ можно безопасно считать
    count = six_search.organic_results.count()

    print(f"✅ Найдено {count} органических результатов, а нам надо >5")
    print(f"Для поиска '{query}' найдено более 5 результатов")
    assert count > 5