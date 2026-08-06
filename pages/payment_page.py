from __future__ import annotations
from models.AutomationExercise_UI_API_Models.payment_detail import PaymentDetails
from pages.base_page import BasePage
from pages.order_confirmation_page import OrderConfirmationPage

class PaymentPage(BasePage):

    def __init__(self, page):
        super().__init__(page)

        self._heading = page.get_by_role("heading", name="Payment")
        self._name = page.locator("[data-qa='name-on-card']")
        self._card = page.locator("[data-qa='card-number']")
        self._cvc = page.locator("[data-qa='cvc']")
        self._month = page.locator("[data-qa='expiry-month']")
        self._year = page.locator("[data-qa='expiry-year']")
        self._confirm = page.locator("[data-qa='pay-button']")


    def is_loaded(self):
        self.wait_for_visibility(self._heading, "Payment Page")

    def enter_payment_details(self, payment: PaymentDetails) -> None:
        self.fill(self._name, payment.name,"Name On Card")
        self.fill(self._card, payment.card_number,"Card Number")
        self.fill(self._cvc, payment.cvc,"CVC Number")
        self.fill(self._month, payment.expiry_month,"Expiry Month")
        self.fill(self._year, payment.expiry_year,"Expiry Year")



    def confirm_order(self)->OrderConfirmationPage:
        self.click(self._confirm, "Confirm Order")

        confirmation = OrderConfirmationPage(self.page)
        confirmation.is_loaded()

        return confirmation

