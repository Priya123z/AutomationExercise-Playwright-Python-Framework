from api.endpoints import Endpoints


def test_get_product_by_id(api_client):

    response = api_client.get(Endpoints.PRODUCTS)

    assert response.ok

    assert response.status == 200

    data = response.json()

    assert "products" in data
