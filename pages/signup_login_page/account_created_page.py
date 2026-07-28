from pages.base_page import BasePage


class AccountCreatedPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self._heading = page.get_by_role("heading",name="Account Created!")
        self._continue_button = page.locator("[data-qa='continue-button']")

    def is_loaded(self):
        self.wait_for_visibility(self._heading, "Account Created Page loaded!")

    def continue_to_home(self):
        self.click(self._continue_button,"Continue to Home Page")
        from pages.home_page import HomePage

        home = HomePage(self.page)
        home.is_loaded()

        return home

