from __future__ import annotations
from playwright.sync_api import Locator, expect
from components.checkout_login_modal import CheckoutModal
from models.AutomationExercise_UI_API_Models.cart_product import CartProduct
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._cart_table = page.locator("#cart_info")
        self._cart_rows = page.locator("#cart_info tbody tr")
        self._empty_cart = page.locator("#empty_cart")
        self._proceed_to_checkout = page.locator("a.check_out")

    def _get_cart_row(self,product_name:str)->Locator:
        return self._cart_rows.filter(
            has=self.page.locator(".cart_description h4 a",has_text=product_name))

    def is_loaded(self)->None:
        self.wait_for_visibility(self._cart_table,"Cart Table")

    def get_product(self, product_name: str) -> CartProduct:
        row = self._get_cart_row(product_name)
        return CartProduct(
            name=row.locator(".cart_description h4 a").inner_text(),
            category = row.locator(".cart_description p").inner_text(),
            price = row.locator(".cart_price p").inner_text(),
            quantity = int(row.locator(".cart_quantity button").inner_text()),
            total = row.locator(".cart_total_price").inner_text()
        )


    def has_product(self, product_name: str) -> bool:
        row = self._get_cart_row(product_name)
        return row.is_visible()

    def remove_product(self, product_name: str) -> None:
        row = self._get_cart_row(product_name)
        self.click(row.locator(".cart_quantity_delete"),f"Removing {product_name}")
        row.wait_for(state="detached")


    def is_empty(self) -> bool:
        return self.is_visible(
            self._empty_cart,
            "Empty Cart"
        )

    def products(self) -> list[CartProduct]:
        products = []

        for i in range(self._cart_rows.count()):
            row = self._cart_rows.nth(i)

            products.append(
                CartProduct(
                    name=row.locator(".cart_description h4 a").inner_text(),
                    category=row.locator(".cart_description p").inner_text(),
                    price=row.locator(".cart_price p").inner_text(),
                    quantity=int(row.locator(".cart_quantity button").inner_text()),
                    total=row.locator(".cart_total_price").inner_text(),
                )
            )

        return products



    def proceed_to_checkout(self) -> CheckoutModal | CheckoutPage:
        from pages.checkout_page import CheckoutPage

        self.click(self._proceed_to_checkout, "Proceed To Checkout")

        checkout_heading = self.page.get_by_role("heading", name ="Address Details")
        checkout_modal = self.page.locator("#checkoutModal")

        expect(checkout_heading.or_(checkout_modal)).to_be_visible()

        if checkout_heading.is_visible():
            checkout = CheckoutPage(self.page)
            checkout.is_loaded()
            return checkout

        modal = CheckoutModal(self.page)
        modal.is_loaded()
        return modal
