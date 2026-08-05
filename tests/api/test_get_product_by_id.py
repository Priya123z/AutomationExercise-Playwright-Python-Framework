def test_get_product_by_id(product_api):

    product_id = 1

    response = product_api.get_product_by_id(product_id)

    assert response.ok
    assert response.status == 200

    data = response.json()

    assert isinstance(data["id"], int)
    assert isinstance(data["title"], str)
    assert isinstance(data["price"], (int, float))
    assert isinstance(data["category"], str)
