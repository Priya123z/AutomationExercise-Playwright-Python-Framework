from models.DummyJsonAPIModels.product import Product
from pages.home_page import HomePage


def test_product_details(page):
    home = HomePage(page)

    products = home.navbar.open_product()

    product_details = products.open_product("Blue Top")

    product_details.is_loaded()

    expected = Product(
        name="Blue Top",
        category="Category: Women > Tops",
        price="Rs. 500",
        availability="Availability: In Stock",
        condition="Condition: New",
        brand="Brand: Polo",
    )

    assert product_details.get_product() == expected
