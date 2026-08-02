from models.cart_product import CartProduct
from pages.home_page import HomePage


def test_verify_product_quantity(page):
    home = HomePage(page)

    products = home.navbar.open_product()

    details = products.open_product("Blue Top")

    details.set_quantity(4)

    cart = details.add_to_cart().view_cart()

    actual = cart.get_product("Blue Top")

    expected = CartProduct(
        name="Blue Top",
        category="Women > Tops",
        price="Rs. 500",
        quantity=4,
        total="Rs. 2000",
    )

    assert actual == expected
    assert actual.total_price == actual.unit_price * actual.quantity