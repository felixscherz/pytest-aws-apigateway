import pytest
import pytest_httpx

from pytest_aws_apigateway.apigateway import ApiGatewayMock


@pytest.fixture
def apigateway_mock(request, httpx_mock: pytest_httpx.HTTPXMock):
    return ApiGatewayMock(httpx_mock)
