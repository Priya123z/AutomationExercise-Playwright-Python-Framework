from models.update_product_request import UpdateProductRequest


def test_update_product_by_flow(product_flow,product_api):
    product_id = product_flow.create_product_and_extract_id(product_api)

    response = product_api.update_product(
        product_id,
        UpdateProductRequest(
            title= "updated iPhone X",
            price= 150000,
            category= "Mobile",
        )
    )

    assert response.status == 200

