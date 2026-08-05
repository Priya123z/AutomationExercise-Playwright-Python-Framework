from dataclasses import asdict
from api.api_client import APIClient
from api.endpoints import Endpoints
from models.login_request import LoginRequest
from utils.logger import logger


class AuthAPI:

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    def login(self, request: LoginRequest):

        logger.info(f"Logging in user: {request.username}")

        return self.api_client.post(
            endpoint=Endpoints.AUTH_LOGIN,
            data=asdict(request)
        )
