from ...pages.github_about_page import AboutPage
import pytest

@pytest.mark.ui
@pytest.mark.smoke
def test_brand_assets(page):
    about_page = AboutPage(page)   # создаём объект страницы About
    about_page.open()              # открываем https://github.com/about

    assert about_page.is_opened() is True  # проверяем что About реально загрузилась

    about_page.click_brand_assets()        # кликаем по карточке Brand assets
    assert "/logo" in page.url             # проверяем что нас перекинуло на страницу Logo (редирект на brand.github.com)

    heading = page.locator("h1", has_text="Logo")
    heading.wait_for(state="visible", timeout=7000)
    assert heading.is_visible()




