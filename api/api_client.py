from playwright.sync_api import APIRequestContext, APIResponse

from utils.logger import logger


class APIClient:

    def __init__(self, request_context: APIRequestContext):
        self.request = request_context

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> APIResponse:

        response =  self.request.get(
            endpoint,
            params=params,
            headers=headers,
        )
        logger.info(f"Response Status: {response.status}")
        return response
