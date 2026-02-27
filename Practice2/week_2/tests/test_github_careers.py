from week_2.pages.github_about_page import AboutPage


def test_careers(page):
    about_page = AboutPage(page)  # создаём объект страницы About
    about_page.open()             # открываем https://github.com/about

    assert about_page.is_opened() is True  # проверяем что About реально загрузилась

    about_page.click_careers()             # кликаем по карточке Careers
    assert "/careers-home" in page.url     # проверяем что произошёл переход на careers сайт

    heading = page.locator('h1[token-data="LP.SKU-A1.HEADER"]')  # локатор главного заголовка Careers страницы
    heading.wait_for(state="visible", timeout=20000)             # ждём пока заголовок реально появится (страница тяжёлая)
    assert heading.is_visible()                                  # финальная проверка: заголовок виден → страница открылась
