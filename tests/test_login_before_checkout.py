from pathlib import Path

import pytest

from models.payment_detail import PaymentDetails

from pages.home_page import HomePage
from utils.test_data import TestData

filepath = Path(__file__).parent.parent.resolve()


payments = TestData.load(filepath /"test_data" /"payments" /"payment.json", model=PaymentDetails)

@pytest.mark.parametrize("payment_details", payments)
def test_login_before_checkout(authenticated_page,payment_details):
    home = HomePage(authenticated_page)
    products = home.navbar.open_product()
    modal = products.add_to_cart("Blue Top")
    cart = modal.view_cart()
    checkout = cart.proceed_to_checkout()
    payment = checkout.place_order()
    payment.enter_payment_details(payment_details)
    confirmation = payment.confirm_order()
    assert confirmation.has_order_placed()
    home  = confirmation.continue_shopping()
    assert home.user_logged_in()
