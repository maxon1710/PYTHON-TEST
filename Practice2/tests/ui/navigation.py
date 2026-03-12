import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config import urls

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get(urls.WIKI_MAIN_URL)
url = driver.current_url
print("URL страницы: ", url)
assert url == urls.WIKI_MAIN_PAGE_URL, "Ошибка в URL"

current_title = driver.title
print("Текущий заголовок: ", current_title)
assert current_title == "Википедия — свободная энциклопедия", "Некорректный title"

time.sleep(3)
