import pytest


@pytest.mark.api
@pytest.mark.products
def test_get_product_by_id(dummyjson_product_api):

    product_id = 1

    response = dummyjson_product_api.get_product_by_id(product_id)

    assert response.ok
    assert response.status == 200

    product = response.json()

    assert product["id"] == product_id
    assert product["title"]
    assert product["price"] > 0
    assert product["category"]
