from pathlib import Path

import pytest

from components.checkout_login_modal import CheckoutModal
from pages.home_page import HomePage
from utils.test_data import TestData


filepath = Path(__file__).parent.parent.resolve()

@pytest.mark.parametrize("user",TestData.load(filepath/"test_data"/"users"/"users.json"))
def test_register_while_checkout(page,user):
    home = HomePage(page)

    products = home.navbar.open_product()

    modal = products.add_to_cart("Blue Top")

    cart = modal.view_cart()

    checkout_modal = cart.proceed_to_checkout()

    login = checkout_modal.register_login()

    login.login(user["email"],user["password"])

    assert home.user_logged_in()

    # Navigate back to cart
    cart = home.navbar.open_cart()

    assert cart.has_product("Blue Top")

    checkout = cart.proceed_to_checkout()

    checkout.is_loaded()





