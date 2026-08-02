from pages.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self._products_heading = page.get_by_role("heading").filter(has_text="All Products")
        self._search_products_input= page.locator("#search_product")
        self._search_products_button = page.locator("#submit_search")
        self._searched_product_result = page.locator(".single-products .productinfo p")
        self._view_product = page.get_by_text("View Product").first

    def is_loaded(self) -> None:
        self.wait_for_visibility(self._products_heading, "Products Heading")
        self.wait_for_visibility(self._search_products_input, "Search Products")

    def search_product(self,value:str) -> None:
        self.fill(self._search_products_input,value, "Search Product")
        self.click(self._search_products_button,"Search click")

    def is_product_displayed(self,value: str)->bool:

        searched_value = self.get_text(self._searched_product_result,"Product name")

        self.is_visible(self._searched_product_result,"Product display")

        return searched_value==value

    def open_product(self):
        from pages.Product_details_page.product_details_page import ProductDetailsPage

        self.click(self._view_product, "Open Product Details")
        product_details = ProductDetailsPage(self.page)
        product_details.is_loaded()

        return product_details




