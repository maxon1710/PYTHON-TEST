from playwright.sync_api import Page
from .base_page import BasePage


class AboutPage(BasePage):
    url = "https://github.com/about"  # URL страницы About для метода open()

    def __init__(self, page: Page):
        super().__init__(page)  # сохраняем вкладку браузера в self.page через BasePage

        self.brand_assets_link = page.locator(
            'a[href*="/logos"]')  # локатор карточки Brand assets

        self.careers_link = page.locator(
            'h2 a[href="https://github.careers/"]')  # локатор карточки Careers (не футер)

    def click_brand_assets(self):
        self.brand_assets_link.click()  # клик по Brand assets → переход на страницу Logo

    def click_careers(self):
        self.careers_link.click()  # клик по Careers → переход на careers сайт

    def is_opened(self) -> bool:
        self.brand_assets_link.wait_for(state="visible", timeout=5000)  # ждём загрузку страницы About
        return "/about" in self.page.url  # проверяем что мы реально на /about
