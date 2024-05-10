from typing import Callable
import httpx
import pytest_httpx
import re

from pytest_aws_apigateway.event import request_to_event, transform_response


class ApiGateway:
    def __init__(self, httpx_mock: pytest_httpx.HTTPXMock):
        self.httpx_mock = httpx_mock
        ...

    def add_integration(
        self, resource: str, method: str, handler: Callable, endpoint: str
    ):
        p = re.compile(r"\{([^\/]+)\}")
        res = re.subn(p, r"([^\/]+)", resource)
        if res[1] > 0:
            newp = re.compile(f"{endpoint}/{res[0]}")
        else:
            newp = endpoint

        resource = resource.lstrip("/")
        resource = f"/{resource}"

        def integration(request: httpx.Request) -> httpx.Response:
            event = request_to_event(request, resource)
            resp = handler(event, None)
            return transform_response(resp)

        self.httpx_mock.add_callback(callback=integration, url=newp, method=method)
