import pytest

from models.AutomationExercise_UI_API_Models.cart_product import CartProduct
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.cart
@pytest.mark.smoke
def test_add_product_to_cart(page):
    home = HomePage(page)

    products = home.navbar.open_product()

    details = products.open_product("Blue Top")
    details.set_quantity(3)

    modal = details.add_to_cart()
    cart = modal.view_cart()

    actual = cart.get_product("Blue Top")

    expected = CartProduct(
        name="Blue Top",
        category="Women > Tops",
        price="Rs. 500",
        quantity=3,
        total="Rs. 1500",
    )

    assert actual == expected
