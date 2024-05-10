import pytest
import pytest_httpx

from pytest_aws_apigateway.apigateway import ApiGateway


@pytest.fixture
def apigateway(request, httpx_mock: pytest_httpx.HTTPXMock):
    return ApiGateway(httpx_mock)
