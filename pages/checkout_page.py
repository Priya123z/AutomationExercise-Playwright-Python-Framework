from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self._checkout_heading = page.get_by_text("Address Details")

    def is_loaded(self) -> None:
        self.wait_for_visibility(self._checkout_heading,"Checkout Page")

