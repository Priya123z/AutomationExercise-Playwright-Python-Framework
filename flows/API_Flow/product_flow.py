from models.DummyJsonAPIModels.create_product_request import CreateProductRequest


class ProductFlow:

    def __init__(self, product_api):
        self.product_api = product_api


    def create_product_and_extract_id(self):

        response = self.product_api.create_product(CreateProductRequest(
            title="iPhone",
            price=1000,
            category="Mobile",
            description="Mobile Phone",
           )

        )



        print(response.status)
        print(response.text())

        assert response.status == 201


        return response.json()["id"]