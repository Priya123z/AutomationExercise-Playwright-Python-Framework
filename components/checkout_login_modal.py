from pages.base_page import BasePage
from pages.signup_login_page.signup_login_page import SignUpLoginPage


class CheckoutModal(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self._modal = page.locator("#checkoutModal")
        self._register_login = page.get_by_role("link",name="Register / Login")
        self._continue_on_cart = page.get_by_role("button",name="Continue On Cart")

    def is_loaded(self) -> None:
        self.wait_for_visibility(self._modal, "Checkout Modal")

    def register_login(self) -> SignUpLoginPage:
        self.click(self._register_login, "Register / Login")

        login = SignUpLoginPage(self.page)
        login.is_loaded()
        return login

    def continue_on_cart(self) -> CartPage:
        from pages.cart_page import CartPage

        self.click(self._continue_on_cart, "Continue On Cart")

        cart = CartPage(self.page)
        cart.is_loaded()
        return cart