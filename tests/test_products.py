from pages.home_page import HomePage


def test_products_page(page):
    home = HomePage(page)

    products = home.navbar.open_product()

    products.is_loaded()


