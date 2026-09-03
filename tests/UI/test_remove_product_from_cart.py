import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.cart
def test_remove_product_from_cart(page):

    home = HomePage(page)

    products = home.navbar.open_product()

    modal = products.add_to_cart("Blue Top")

    cart = modal.view_cart()

    assert cart.has_product("Blue Top")

    cart.remove_product("Blue Top")

    assert cart.is_empty()
