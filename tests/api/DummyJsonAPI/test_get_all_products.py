import pytest



@pytest.mark.api
@pytest.mark.products
@pytest.mark.smoke
def test_get_all_products(dummyjson_product_api):

    response = dummyjson_product_api.get_all_products()

    assert response.ok

    assert response.status == 200

    data = response.json()

    products = data["products"]

    assert isinstance(products,list)

    assert "products" in data

    assert len(products) > 0

    first_product = products[0]

    assert isinstance(first_product["id"], int)
    assert isinstance(first_product["title"], str)
    assert isinstance(first_product["price"], (int, float))


