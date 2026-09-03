import pytest

@pytest.mark.api
@pytest.mark.products
def test_delete_product(dummyjson_product_api):

    product_id = 1

    response = dummyjson_product_api.delete_product(product_id)

    assert response.ok
    assert response.status == 200

    data = response.json()

    assert data["id"] == product_id
    assert data["isDeleted"] is True
