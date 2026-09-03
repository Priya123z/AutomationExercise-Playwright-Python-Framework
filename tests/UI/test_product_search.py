import pytest

from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.products
def test_search_product(page):
    home = HomePage(page)

    products = home.navbar.open_product()

    products.search_product("Blue Top")

    assert products.is_product_displayed("Blue Top")
