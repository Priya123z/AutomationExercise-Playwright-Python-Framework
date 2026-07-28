from pages.base_page import BasePage


class APITestPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
    def is_loaded(self):
        pass
