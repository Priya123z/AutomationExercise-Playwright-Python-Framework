import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.products
def test_products_page(page):
    home = HomePage(page)

    products = home.navbar.open_product()

    products.is_loaded()


