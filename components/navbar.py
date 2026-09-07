from pages.base_page import BasePage
from pages.cart_page import CartPage


class Navbar(BasePage):

    """
    Reusable navigation component shared across all pages.
    """
    def __init__(self, page):
        super().__init__(page)
        self._product_link = page.get_by_role("link", name = "Products")
        self._cart_link = self.page.locator('a[href="/view_cart"]').first
        self._signup_link = page.get_by_role("link", name="Signup / Login")
        self._logout_link = page.get_by_role("link", name="Logout")


    def open_product(self):
        from pages.product_page import ProductPage
        self.click(self._product_link, "Redirecting to ProductPage")
        product_page = ProductPage(self.page)
        product_page.is_loaded()
        return product_page

    def open_cart(self):
        self.click(self._cart_link, "Redirecting to CartPage")
        cart_page = CartPage(self.page)
        cart_page.is_loaded()
        return cart_page

    def open_signup_login(self):
        from pages.signup_login_page.signup_login_page import SignUpLoginPage
        self.click(self._signup_link, "Redirecting to SignUpPage")
        signup_login_page = SignUpLoginPage(self.page)
        signup_login_page.is_loaded()
        return signup_login_page

    def logout(self):
        from pages.signup_login_page.signup_login_page import SignUpLoginPage
        self.click(self._logout_link, "Redirecting to HomePage")
        logout_page = SignUpLoginPage(self.page)
        logout_page.is_loaded()
        return logout_page


