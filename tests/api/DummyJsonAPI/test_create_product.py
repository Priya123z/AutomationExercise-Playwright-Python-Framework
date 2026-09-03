import pytest

from utils.schema_validator import SchemaValidator


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.products
def test_create_product(dummyjson_product_api, create_product_request):

    response = dummyjson_product_api.create_product(create_product_request)

    assert response.ok
    assert response.status == 201

    SchemaValidator.validate_response(response, "product/create_product_schema.json")

    product = response.json()

    assert product["title"] == create_product_request.title
    assert product["price"] == create_product_request.price
    assert product["category"] == create_product_request.category
