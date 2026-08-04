from api.endpoints import Endpoints


def test_get_all_products(api_client):

    response = api_client.get(Endpoints.PRODUCTS)

    assert response.ok

    assert response.status == 200

    data = response.json()

    assert "products" in data

    products = data["products"]

    assert len(products) > 0

    first_product = products[0]

    assert "id" in first_product
    assert "title" in first_product
    assert "price" in first_product