from components.navbar import Navbar
from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self.navbar = Navbar(page)
        self._home_banner = page.locator("#slider")
        self._featured_products = page.get_by_role("heading",name="Features Items")
        self._subscription = page.get_by_role("heading",name="Subscription")
        self._logged_user = page.locator("a").filter(has_text="Logged in as")


    def is_loaded(self):
        self.wait_for_visibility(self._home_banner,"Home Banner")
        self.wait_for_visibility(self._featured_products,"Featured Products")
        self.wait_for_visibility(self._subscription,"Subscription")


    def user_logged_in(self):
        return self.is_visible(self._logged_user, "Logged in")

