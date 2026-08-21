from __future__ import annotations

from playwright.sync_api import expect
from pages.base_page import BasePage
from pages.cart_page import CartPage
from utils.config_manager import config


class CartModal(BasePage):
    def __init__(self, page):
        super().__init__(page)
        #locators:
        self._modal = page.locator("#cartModal")
        self._continue_shopping = page.get_by_role("button",name = "Continue Shopping")
        self._view_cart = page.get_by_role("link",name="View Cart")

    def is_loaded(self)->None:
        self.wait_for_visibility(self._modal, "Cart Modal")
        self.wait_for_visibility(self._view_cart, "View Cart")

    def wait_until_loaded(self):
        expect(self._modal).to_be_visible(timeout=config.expect_timeout)

    def continue_shopping(self)->ProductPage:
        from pages.product_page import ProductPage

        self.click(self._continue_shopping,"Continue shopping")
        products = ProductPage(self.page)
        return products


    def view_cart(self)->CartPage:
        self.click(self._view_cart,"View Cart")
        cart = CartPage(self.page)
        cart.is_loaded()
        return cart
