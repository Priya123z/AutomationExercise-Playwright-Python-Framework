from pages.base_page import BasePage
from models.product import Product

class ProductDetailsPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self._product_name = page.locator(".product-information h2")
        self._category = page.locator(".product-information p").filter(has_text="Category:")
        self._price = page.locator(".product-information span span")
        self._availability = page.locator(".product-information p").filter(has_text="Availability:")
        self._condition = page.locator(".product-information p").filter(has_text="Condition:")
        self._brand = page.locator(".product-information p").filter(has_text="Brand:")


    def is_loaded(self):
        self.wait_for_visibility(self._product_name, "Product Name")
        self.wait_for_visibility(self._category, "Product Category")
        self.wait_for_visibility(self._price, "Product Price")
        self.wait_for_visibility(self._availability, "Product Availability")
        self.wait_for_visibility(self._condition, "Product Condition")
        self.wait_for_visibility(self._brand, "Product Brand")


    def get_product(self)->Product:
        return Product(
            name = self.get_text(self._product_name, "Product Name"),
            category = self.get_text(self._category, "Product Category"),
            price = self.get_text(self._price, "Product Price"),
            availability = self.get_text(self._availability, "Product Availability"),
            condition = self.get_text(self._condition, "Product Condition"),
            brand = self.get_text(self._brand, "Product Brand")

        )


