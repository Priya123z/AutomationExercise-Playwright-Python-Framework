from playwright.sync_api import Page

from components.navbar import Navbar
from pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.navbar = Navbar(page)
        self._home_banner = page.locator("#slider")
        self._featured_products = page.get_by_role("heading",name="Features Items")
        self._subscription = page.get_by_role("heading",name="Subscription")

    def is_loaded(self) -> None:
        self.wait_for_visibility(self._home_banner,"Home Banner")
        self.wait_for_visibility(self._featured_products,"Featured Products")
        self.wait_for_visibility(self._subscription,"Subscription")


    def _verify_home_banner(self)->None:
        self.is_visible(self._home_banner,"Home Banner")

    def _verify_featured_products(self)->None:
        self.is_visible(self._featured_products,"Featured Products")

    def _verify_subscription(self)->None:
        self.is_visible(self._subscription,"Subscription")

    def validate_home_page(self)->None:
        self._verify_home_banner()
        self._verify_featured_products()
        self._verify_subscription()
