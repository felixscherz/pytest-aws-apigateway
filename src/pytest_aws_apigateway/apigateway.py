import json
import re
from typing import Any
from typing import Callable
from typing import Union

import httpx
import pytest_httpx

from pytest_aws_apigateway.context import LambdaContext
from pytest_aws_apigateway.context import create_context
from pytest_aws_apigateway.integration import Integration, IntegrationResponse
from pytest_aws_apigateway.integration import ResponseFormatError
from pytest_aws_apigateway.integration import build_integration_request
from pytest_aws_apigateway.integration import transform_integration_response

__all__ = ["ApiGatewayMock"]


class ApiGatewayMock:
    """Mock acting as an AWS ApiGateway for AWS Lambda prox integrations."""

    def __init__(self, httpx_mock: pytest_httpx.HTTPXMock):
        self.httpx_mock = httpx_mock
        ...

    def add_integration(
        self,
        resource: str,
        method: str,
        endpoint: str,
        handler: Callable[[dict[str, Any], LambdaContext], IntegrationResponse],
    ) -> Integration:
        """
        Register an AWS Lambda function handler that will be called if a request matches.

        Args:
            resource: Resource path where to mount the integration. Will be combined with endpoint to match request URLs
            method: HTTP method for which the integration should be called. Can be 'ANY' as a catch-all.
            endpoint: API endpoint for the API gateway. Example: 'http://localhost'
            handler: AWS Lambda handler function that will be called when a request matches
        """
        resource = self._normalize_resource(resource)
        endpoint = self._normalize_endpoint(endpoint)

        url = self._url_expression(endpoint, resource)

        def integration(request: httpx.Request) -> httpx.Response:
            event = build_integration_request(request, resource)
            context = create_context(handler)
            resp = handler(event, context)
            try:
                return transform_integration_response(resp)
            except ResponseFormatError:
                return httpx.Response(
                    status_code=500,
                    json=json.dumps({"message": "Internal server error"}),
                )

        method_to_match = method.upper()
        if method_to_match == "ANY":
            method_to_match = None
        self.httpx_mock.add_callback(
            callback=integration, url=url, method=method_to_match
        )
        return Integration(resource, method.upper(), endpoint)

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
