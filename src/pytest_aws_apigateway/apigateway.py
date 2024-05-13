import json
import re
from typing import Callable
from typing import Union

import httpx
import pytest_httpx

from pytest_aws_apigateway.context import LambdaContext, create_context
from pytest_aws_apigateway.event import OutputFormatError
from pytest_aws_apigateway.event import request_to_event
from pytest_aws_apigateway.event import transform_response

__all__ = ["ApiGatewayMock"]


class ApiGatewayMock:
    def __init__(self, httpx_mock: pytest_httpx.HTTPXMock):
        self.httpx_mock = httpx_mock
        ...

    def add_integration(
        self,
        resource: str,
        method: str,
        endpoint: str,
        handler: Callable[[dict, LambdaContext], Union[dict, httpx.Response]],
    ):
        resource = self._normalize_resource(resource)
        endpoint = self._normalize_endpoint(endpoint)

        url = self._url_expression(endpoint, resource)
        print(resource)
        print(url)

        def integration(request: httpx.Request) -> httpx.Response:
            event = request_to_event(request, resource)
            context = create_context(handler)
            resp = handler(event, context)
            try:
                return transform_response(resp)
            except OutputFormatError:
                return httpx.Response(
                    status_code=500,
                    json=json.dumps({"message": "Internal server error"}),
                )

        self.httpx_mock.add_callback(callback=integration, url=url, method=method)

    def _normalize_resource(self, resource: str) -> str:
        resource = resource.lstrip("/")
        resource = f"/{resource}"
        return resource

    def _url_expression(self, endpoint: str, resource: str) -> Union[re.Pattern, str]:
        p = re.compile(r"\{([^\/]+)\}")
        res = re.subn(p, r"([^\/]+)", resource)
        return re.compile(f"{endpoint}{res[0]}")

    def _normalize_endpoint(self, endpoint: str) -> str:
        return endpoint.rstrip("/")
