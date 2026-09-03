from __future__ import annotations
from pathlib import Path

import pytest

from models.AutomationExercise_UI_API_Models.payment_detail import PaymentDetails
from pages.home_page import HomePage
from utils.test_data import TestData

filepath = Path(__file__).parent.parent.parent.resolve()

payments = TestData.load(filepath / "test_data" / "payments" / "payment.json", model=PaymentDetails)


@pytest.mark.ui
@pytest.mark.checkout
@pytest.mark.parametrize("payment_details", payments)
def test_register_while_checkout(page, registered_user, payment_details):
    home = HomePage(page)

    products = home.navbar.open_product()

    modal = products.add_to_cart("Blue Top")

    cart = modal.view_cart()

    checkout_modal = cart.proceed_to_checkout()

    login = checkout_modal.register_login()

    login.login(registered_user.email, registered_user.password)

    assert home.user_logged_in()

    cart = home.navbar.open_cart()

    assert cart.has_product("Blue Top")

    checkout = cart.proceed_to_checkout()

    payment = checkout.place_order()

    payment.is_loaded()

    payment.enter_payment_details(payment_details)

    confirmation = payment.confirm_order()

    confirmation.is_loaded()

    assert confirmation.has_order_placed()

    home = confirmation.continue_shopping()

    assert home.user_logged_in()
