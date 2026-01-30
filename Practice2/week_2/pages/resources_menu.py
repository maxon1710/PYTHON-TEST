from playwright.sync_api import Page


class ResourcesMenu:
    def __init__(self, page: Page):
        self.page = page

        # Заголовок секции Explore by topic
        self.topics_heading = page.locator(
            'span:has-text("EXPLORE BY TOPIC")'
        )

        # Ссылки внутри списка Topics
        self.topics_links = self.topics_heading.locator(
            "xpath=following-sibling::ul[1]//a"
        )

    def get_topics_texts(self) -> list[str]:
        """
        Собираем все названия топиков из меню
        """
        self.topics_links.first.wait_for(state="visible", timeout=7000)
        return self.topics_links.all_inner_texts()
