import pytest

from models.DummyJsonAPIModels.update_product_request import UpdateProductRequest


@pytest.mark.api
@pytest.mark.products
def test_update_product_by_flow(product_flow, dummyjson_product_api):

    product_id = product_flow.get_product_id()

    response = dummyjson_product_api.update_product(
        product_id,
        UpdateProductRequest(
            title="Updated iPhone",
            price=150000,
            category="Mobile"
        )
    )

    assert response.status == 200

    updated_product = response.json()

    assert updated_product["id"] == product_id
    assert updated_product["title"] == "Updated iPhone"
    assert updated_product["price"] == 150000
    assert updated_product["category"] == "Mobile"
