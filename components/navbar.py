from __future__ import annotations
from pages.api_test_case_page import APITestPage
from pages.contact_us_page import ContactUsPage
from pages.base_page import BasePage
from pages.cart_page import CartPage
from pages.test_case_page import TestCasePage
from pages.videotutorialspage import VideoTutorialsPage


class Navbar(BasePage):

    """
    Reusable navigation component shared across all pages.
    """
    def __init__(self, page):
        super().__init__(page)
        self._home_link = page.get_by_role("link", name = "Home")
        self._product_link = page.get_by_role("link", name = "Products")
        self._cart_link = self.page.locator('a[href="/view_cart"]').first
        self._signup_link = page.get_by_role("link", name="Signup / Login")
        self._contact_us_link = page.get_by_role("link", name = "Contact us")
        self._test_cases_link = page.locator("a").filter(has_text="Test Cases").first
        self._api_test_cases_link = page.get_by_role("link", name="API Testing")
        self._video_tutorials_link = page.get_by_role("link", name="Video Tutorials")
        self._logout_link = page.get_by_role("link", name="Logout")
        self._delete_account = page.get_by_role("link", name="Delete Account")


    def open_home(self):
        from pages.home_page import HomePage
        self.click(self._home_link, "Redirecting to HomePage")
        home_page = HomePage(self.page)
        home_page.is_loaded()
        return home_page

    def open_product(self):
        from pages.product_page import ProductPage
        self.click(self._product_link, "Redirecting to ProductPage")
        product_page = ProductPage(self.page)
        product_page.is_loaded()
        return product_page

    def open_cart(self)-> CartPage:
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


    def open_contact_us(self)->ContactUsPage:
        self.click(self._contact_us_link, "Redirecting to ContactUsPage")
        contact_us_page = ContactUsPage(self.page)
        contact_us_page.is_loaded()
        return contact_us_page

    def open_test_cases(self)->TestCasePage:
        self.click(self._test_cases_link, "Redirecting to TestCasesPage")
        test_cases_page = TestCasePage(self.page)
        test_cases_page.is_loaded()
        return test_cases_page

    def open_api_test_cases(self)->APITestPage:
        self.click(self._api_test_cases_link, "Redirecting to APITestCasesPage")
        api_test_case_page = APITestPage(self.page)
        api_test_case_page.is_loaded()
        return api_test_case_page

    def open_video_tutorials(self)->VideoTutorialsPage:
        self.click(self._video_tutorials_link, "Redirecting to VideoTutorialsPage")
        video_tutorials_page = VideoTutorialsPage(self.page)
        video_tutorials_page.is_loaded()
        return video_tutorials_page
    
    def logout(self):
        from pages.signup_login_page.signup_login_page import SignUpLoginPage
        self.click(self._logout_link, "Redirecting to HomePage")
        logout_page = SignUpLoginPage(self.page)
        logout_page.is_loaded()
        return logout_page


