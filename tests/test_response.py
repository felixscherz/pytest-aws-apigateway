from httpx import Response

from pytest_aws_apigateway.event import transform_response


def test_transform_response():
    output = {"statusCode": 200}
    response = transform_response(output)
    assert isinstance(response, Response)
