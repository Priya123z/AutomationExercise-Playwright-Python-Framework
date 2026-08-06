def test_update_product(product_api, update_product_request):

    product_id = 1

    response = product_api.update_product(
        product_id=product_id,
        request=update_product_request,
    )

    assert response.ok
    assert response.status == 200

    product = response.json()

    assert product["id"] == product_id
    assert product["title"] == update_product_request.title
    assert product["price"] == update_product_request.price
    assert product["category"] == update_product_request.category