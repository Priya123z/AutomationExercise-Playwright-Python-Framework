from pages.base_page import BasePage
from pages.signup_login_page.signup_login_page import SignUpLoginPage


class CheckoutModal(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self._modal = page.locator("#checkoutModal")
        self._register_login = page.get_by_role("link",name="Register / Login")

    def is_loaded(self):
        self.wait_for_visibility(self._modal, "Checkout Modal")

    def register_login(self):
        self.click(self._register_login, "Register / Login")

        login = SignUpLoginPage(self.page)
        login.is_loaded()
        return login