from dataclasses import asdict

from api.endpoints import Endpoints
from utils.logger import logger


class DummyJsonAuthAPI:

    def __init__(self, api_client):
        self.api_client = api_client

    def login(self, request):

        logger.info(f"Logging in user: {request.username}")

        return self.api_client.post(
            endpoint=Endpoints.AUTH_LOGIN,
            data=asdict(request),
        )
