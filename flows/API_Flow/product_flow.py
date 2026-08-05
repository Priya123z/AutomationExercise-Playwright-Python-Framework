from models.create_product_request import CreateProductRequest


class ProductFlow:

    def create_product_and_extract_id(self, product_api):

        response = product_api.create_product(CreateProductRequest(
            title="iPhone",
            price=1000,
            category="Mobile",
            description="Mobile Phone",
           )

        )

        assert response.status == 201

        product_id = response.json()["id"]

        print(response.status)
        print(response.json())

        return product_id