from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self._checkout_heading = page.get_by_role("heading", name="Address Details")
        self._place_order = page.locator("a.check_out")

    def is_loaded(self):
        self.wait_for_visibility(self._checkout_heading, "Checkout Page")

    def place_order(self):
        self.click(self._place_order, "Place Order")

        from pages.payment_page import PaymentPage

        payment = PaymentPage(self.page)
        payment.is_loaded()
        return payment