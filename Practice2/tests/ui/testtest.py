import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import urls

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(urls.YANDEX_WEATHER_URL)
url = driver.current_url


print("Открыт URL = ", url)
assert url == driver.current_url

title = driver.title
print("Заголовок страницы:", title)
assert  title == "Погода в Санкт-Петербурге — Прогноз погоды в Санкт-Петербурге, Россия"
