from pages.base_page import BasePage
from pages.home_page import HomePage


class OrderConfirmationPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self._success_message = page.locator("[data-qa='order-placed']")
        self._continue = page.locator("[data-qa='continue-button']")

    def is_loaded(self):
        self.wait_for_visibility(
            self._success_message,
            "Order Confirmation"
        )

    def continue_shopping(self):
        self.click(self._continue, "Continue")
        home = HomePage(self.page)
        home.is_loaded()
        return home

    def has_order_placed(self):
        return self.get_text(self._success_message,"Success message for order placement" ) == "Order Placed!"
