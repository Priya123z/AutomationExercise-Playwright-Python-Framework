import pytest


@pytest.mark.api
@pytest.mark.products
@pytest.mark.smoke
def test_get_all_products(dummyjson_product_api):

    response = dummyjson_product_api.get_all_products()

    assert response.ok
    assert response.status == 200

    products = response.json()["products"]

    assert products, "the catalogue came back empty"

    first_product = products[0]

    assert first_product["id"]
    assert first_product["title"]
    assert first_product["price"] > 0
