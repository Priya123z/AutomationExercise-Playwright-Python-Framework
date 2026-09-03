import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.cart
def test_add_multiple_products(page):
    home = HomePage(page)
    products = home.navbar.open_product()
    modal = products.add_to_cart("Blue Top")

    products = modal.continue_shopping()

    modal = products.add_to_cart("Men Tshirt")

    cart = modal.view_cart()

    assert cart.has_product("Blue Top")
    assert cart.has_product("Men Tshirt")




