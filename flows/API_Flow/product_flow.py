class ProductFlow:

    def __init__(self, dummyjson_product_api):
        self.dummyjson_product_api = dummyjson_product_api

    def get_product_id(self):

        response = self.dummyjson_product_api.get_all_products()

        assert response.status == 200

        return response.json()["products"][0]["id"]
