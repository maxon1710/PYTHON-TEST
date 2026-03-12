from playwright.sync_api import Page

from config import urls
from config.settings import UI_TIMEOUT_MS
from .base_page import BasePage


class AboutPage(BasePage):
    url = urls.GITHUB_ABOUT_URL  # URL страницы About для метода open()

    def __init__(self, page: Page):
        super().__init__(page)  # сохраняем вкладку браузера в self.page через BasePage

        self.brand_assets_link = page.locator(
            'a[href*="/logos"]')  # локатор карточки Brand assets

        self.careers_link = page.locator(
            f'h2 a[href="{urls.GITHUB_CAREERS_URL}"]')  # локатор карточки Careers (не футер)

    def click_brand_assets(self):
        self.brand_assets_link.click()  # клик по Brand assets → переход на страницу Logo

    def click_careers(self):
        self.careers_link.click()  # клик по Careers → переход на careers сайт

    def is_opened(self) -> bool:
        self.brand_assets_link.wait_for(state="visible", timeout=UI_TIMEOUT_MS)  # ждём загрузку страницы About
        return "/about" in self.page.url  # проверяем что мы реально на /about
