def test_get_invalid_product(dummyjson_product_api):

    response = dummyjson_product_api.get_product_by_id(999999)

    assert response.status == 404

    data = response.json()

    assert data["message"] == "Product with id '999999' not found"
