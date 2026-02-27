import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://yandex.ru/pogoda/ru/saint-petersburg")
url = driver.current_url


print("Открыт URL = ", url)
assert url == driver.current_url

title = driver.title
print("Заголовок страницы:", title)
assert  title == "Погода в Санкт-Петербурге — Прогноз погоды в Санкт-Петербурге, Россия"