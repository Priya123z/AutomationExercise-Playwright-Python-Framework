from playwright.sync_api import Locator, expect

from components.cart_modal import CartModal
from pages.base_page import BasePage
from pages.product_details_page import ProductDetailsPage


class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._products_heading = page.get_by_role("heading").filter(has_text="All Products")
        self._search_products_input = page.locator("#search_product")
        self._search_products_button = page.locator("#submit_search")
        self._product_cards = page.locator(".product-image-wrapper")

    def is_loaded(self) -> None:
        self.wait_for_visibility(self._products_heading, "Products Heading")
        self.wait_for_visibility(self._search_products_input, "Search Products")

    def search_product(self, value: str) -> None:
        self.fill(self._search_products_input,value,"Search Product")
        self.click(self._search_products_button,"Search click")

    def is_product_displayed(self, value: str) -> bool:
        product = self._product_cards.filter(has=self.page.locator("p", has_text=value)).first

        product_name = product.locator("p", has_text=value).first

        expect(product_name).to_be_visible()
        return product_name.is_visible()

    def _get_product_card(self, product_name: str) -> Locator:
        return self._product_cards.filter(has=self.page.locator(".productinfo p", has_text=product_name)).first

    def open_product(self, product_name: str) -> ProductDetailsPage:
        product = self._get_product_card(product_name)

        self.click(product.get_by_role("link", name="View Product"),f"Opening {product_name}")

        details = ProductDetailsPage(self.page)
        details.is_loaded()

        return details

    def add_to_cart(self, product_name: str) -> CartModal:
        product = self._get_product_card(product_name)

        product.scroll_into_view_if_needed()
        product.hover()

        add_to_cart = product.locator(".overlay-content").get_by_text("Add to cart",exact=True)

        add_to_cart.click()

        modal = CartModal(self.page)
        modal.wait_until_loaded()

        return modal