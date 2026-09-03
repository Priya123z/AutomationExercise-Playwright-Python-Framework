from models.DummyJsonAPIModels.create_product_request import CreateProductRequest


class ProductFlow:

    def __init__(self, dummyjson_product_api):
        self.dummyjson_product_api = dummyjson_product_api


    def create_product_and_extract_id(self):

        response = self.dummyjson_product_api.create_product(CreateProductRequest(
            title="iPhone",
            price=1000,
            category="Mobile",
            description="Mobile Phone",
           )

        )

        assert response.status == 201

        return response.json()["id"]

    def get_product_id(self):

        response = self.dummyjson_product_api.get_all_products()

        assert response.status == 200

        return response.json()["products"][0]["id"]
