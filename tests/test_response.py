from httpx import Response

from pytest_aws_apigateway.integration import transform_integration_response


def test_transform_response():
    output = {"statusCode": 200}
    response = transform_integration_response(output)
    assert isinstance(response, Response)
