from models.DummyJsonAPIModels.update_product_request import UpdateProductRequest


def test_update_product_by_flow(product_flow, product_api):

    product_id = product_flow.create_product_and_extract_id()

    response = product_api.update_product(
        product_id,
        UpdateProductRequest(
            title="Updated iPhone",
            price=150000,
            category="Mobile"
        )
    )

    assert response.status == 200