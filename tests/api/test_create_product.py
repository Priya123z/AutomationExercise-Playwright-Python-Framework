def test_create_product(product_api, create_product_request):

    response = product_api.create_product(create_product_request)

    assert response.ok
    assert response.status == 201

    product = response.json()

    assert product["title"] == create_product_request.title
    assert product["price"] == create_product_request.price
    assert product["category"] == create_product_request.category


    assert "id" in product