import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from config import urls

@pytest.mark.ui
@pytest.mark.external
def test_footer_resources():
    driver = webdriver.Chrome()
    driver.get(urls.GITHUB_BASE_URL)


    # Находим resources в футере и жмем
    driver.find_element(
        By.XPATH,"//footer//a[normalize-space()='Resources']").click()
    resources_url = driver.current_url
    assert resources_url == urls.GITHUB_RESOURCES_URL
    print("Редирект на:", resources_url)

    # находим "Topics" в шапке и жмем с поиском списка
    driver.find_element(
        By.XPATH, "//button[@aria-label='Show the Topics dropdown menu']").click()
    time.sleep(5)

    topics_links = driver.find_elements(
        By.XPATH, "//ul[contains(@class,'site-navigation__dropdown')]//a")
    actual_topics = [link.text for link in topics_links if link.text.strip() != ""]
    print("ACTUAL TOPICS:", actual_topics)

    expected_topics = [
        "AI",
        "Software Development",
        "DevOps",
        "Security",
        "View all topics"
    ]

    for topic in expected_topics:  # берём каждую ожидаемую тему по очереди
        assert topic in actual_topics, f"❌ Missing topic: {topic}" # проверяем, что она реально есть в меню

    print('Успешно: Все нужные темы из задания найдены в дропдауне "Resources"')
