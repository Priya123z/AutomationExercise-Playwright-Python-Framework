from dataclasses import asdict

from api.endpoints import Endpoints
from utils.logger import logger


class ProductAPI:

    def __init__(self, api_client):
        self.api_client = api_client

    def get_all_products(self):

        logger.info("Getting all products")

        return self.api_client.get(
            Endpoints.PRODUCTS
        )

    def get_product_by_id(self, product_id):

        logger.info(f"Getting product {product_id}")

        endpoint = Endpoints.PRODUCT.format(id=product_id)

        return self.api_client.get(endpoint)

    def create_product(self, request):

        logger.info(f"Creating product: {request.title}")

        return self.api_client.post(
            endpoint=Endpoints.ADD_PRODUCT,
            data=asdict(request),
        )

    def update_product(self, product_id, request):

        logger.info(f"Updating Product: {product_id}")

        endpoint = Endpoints.PRODUCT.format(id=product_id)

        return self.api_client.patch(endpoint, data=asdict(request))

    def delete_product(self, product_id):

        logger.info(f"Deleting Product: {product_id}")

        endpoint = Endpoints.PRODUCT.format(id=product_id)

        return self.api_client.delete(endpoint)
