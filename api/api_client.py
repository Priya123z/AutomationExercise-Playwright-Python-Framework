from enum import StrEnum
from urllib.parse import urljoin

from playwright.sync_api import APIRequestContext, APIResponse

from utils.config_manager import config
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
            method:HttpMethod,
            endpoint,
            data=None,
            form=None,
            params=None,
            headers=None,
    ):


        url = str(urljoin(config.api_base_url + "/", endpoint))

        response = self.request.fetch(
            url,
            method=method,
            form=form,
            data=data,
            params=params,
            headers=headers,
        )


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
            form: dict | None = None,
    ) -> APIResponse:

        return self._send_request(method = HttpMethod.POST,
                                  endpoint=endpoint,
                                  data=data,
                                  headers=headers,
                                  form=form)



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
            data: dict | None = None,
            form: dict | None = None,
            headers: dict | None = None,

    ) -> APIResponse:


        return self._send_request(
            method=HttpMethod.DELETE,
            endpoint=endpoint,
            data=data,
            form=form,
            headers=headers)

