import time
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

    MAX_ATTEMPTS = 4
    BACKOFF_SECONDS = 2

    def __init__(self,request_context: APIRequestContext,base_url: str,):
        self.request = request_context
        self.base_url = base_url or config.api_base_url

    def _send_request(
            self,
            method:HttpMethod,
            endpoint,
            data=None,
            form=None,
            params=None,
            headers=None,
    ):
        url = str(urljoin(self.base_url + "/", endpoint))

        response = self._fetch_with_backoff(method, url, data, form, params, headers)

        self._reject_non_json(response, method, url)

        return response

    def _fetch_with_backoff(self, method, url, data, form, params, headers):
        """Retry 429 and 5xx, nothing else.

        These run against public APIs from a shared CI runner, so being rate
        limited is a fact of the environment rather than a defect in the code under
        test. 4xx is never retried, because the negative tests assert on those and
        retrying a 404 would break them.
        """
        for attempt in range(1, self.MAX_ATTEMPTS + 1):
            response = self.request.fetch(
                url,
                method=method,
                form=form,
                data=data,
                params=params,
                headers=headers,
            )

            retryable = response.status == 429 or response.status >= 500

            if not retryable or attempt == self.MAX_ATTEMPTS:
                return response

            wait = self.BACKOFF_SECONDS * attempt
            logger.warning(
                f"{method} {url} returned {response.status}, retrying in {wait}s "
                f"(attempt {attempt} of {self.MAX_ATTEMPTS})"
            )
            time.sleep(wait)

        return response

    @staticmethod
    def _reject_non_json(response: APIResponse, method: HttpMethod, url: str) -> None:
        """Fail with the reason rather than letting response.json() blow up later.

        automationexercise.com is behind Cloudflare, which serves an HTML challenge
        to datacenter addresses. On a CI runner that used to surface twenty rows of
        `JSONDecodeError: Expecting value: line 1 column 1`, which says nothing
        about what actually happened.
        """
        body = response.text().lstrip()

        if body[:1] in ("{", "["):
            return

        snippet = " ".join(body[:160].split())

        raise AssertionError(
            f"{method} {url} returned {response.status} but the body is not JSON. "
            f"This is usually a bot challenge rather than a defect  the site sits "
            f"behind Cloudflare and answers datacenter addresses differently. "
            f"Body starts: {snippet!r}"
        )

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

