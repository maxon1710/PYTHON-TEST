from pages.github_public_home_page import GitHubPublicHomePage
import pytest

@pytest.mark.ui
@pytest.mark.smoke
def test_topics_in_resources_menu(page):
    home_page = GitHubPublicHomePage(page)   # создаём объект главной страницы GitHub
    home_page.open()                         # открываем https://github.com/

    resources_menu = home_page.open_resources_menu()  # наводим мышь на Resources → появляется меню

    actual_topics = resources_menu.get_topics_texts() # собираем реальные пункты Topics со страницы

    expected_topics = [                      # список тем, которые ОБЯЗАНЫ быть в меню
        "AI",
        "DevOps",
        "Security",
        "Software Development",
        "View all topics",
    ]

    for topic in expected_topics:             # берём каждую ожидаемую тему по очереди
        assert topic in actual_topics         # проверяем, что она реально есть в меню

    print("ACTUAL TOPICS:", actual_topics)
