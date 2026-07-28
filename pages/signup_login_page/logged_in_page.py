from pages.base_page import BasePage


class LoggedInPage(BasePage):

    def __init__(self,page):
        super().__init__(page)
    def is_loaded(self):
        pass


