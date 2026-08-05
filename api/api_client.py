from enum import StrEnum

from playwright.sync_api import APIRequestContext, APIResponse

from utils.logger import logger


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"

class APIClient:


    def __init__(self, request_context: APIRequestContext):
        self.request = request_context

    def _send_request(
            self,
            method: HttpMethod,
            endpoint: str,
            data: dict | None = None,
            params: dict | None = None,
            headers: dict | None = None,
    ) -> APIResponse:

        logger.info(f"{method} {endpoint}")

        response = self.request.fetch(
            endpoint,
            method=method,
            data=data,
            params=params,
            headers=headers,
        )

        logger.info(f"Response Status: {response.status}")

        return response

    def get(
        self,
        endpoint: str,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> APIResponse:

        return self._send_request(method=HttpMethod.GET,
                                  endpoint=endpoint,
                                  params=params,
                                  headers=headers)

    def post(
            self,
            endpoint: str,
            data: dict | None = None,
            headers: dict | None = None,
    ) -> APIResponse:

        return self._send_request(method = HttpMethod.POST,
                                  endpoint=endpoint,
                                  data=data,
                                  headers=headers)

    def put(
            self,
            endpoint: str,
            data: dict | None = None,
            headers: dict | None = None,
    ) -> APIResponse:



        return self._send_request(method = HttpMethod.PUT,
                                  endpoint=endpoint,
                                  data=data,
                                  headers=headers)


    def patch(
            self,
            endpoint: str,
            data: dict | None = None,
            headers: dict | None = None,
    ) -> APIResponse:

        return self._send_request(method = HttpMethod.PATCH,
                                  endpoint=endpoint,
                                  data=data,
                                  headers=headers)

    def delete(
            self,
            endpoint: str,
            headers: dict | None = None,
    ) -> APIResponse:

        return self._send_request(method = HttpMethod.DELETE,
                                  endpoint=endpoint,
                                  headers=headers)