import httpx

from pytest_aws_apigateway import ApiGatewayMock


def test_handler(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return httpx.Response(200, json={"body": "hello"})

    apigateway_mock.add_integration(
        "/", handler=handler, method="GET", endpoint="https://some/"
    )

    with httpx.Client() as client:
        resp = client.get("https://some/")
        assert resp.json() == {"body": "hello"}


def test_invalid_output_format_returns_500(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": "200"}

    apigateway_mock.add_integration(
        "/", handler=handler, method="GET", endpoint="https://some/"
    )

    with httpx.Client() as client:
        resp = client.get("https://some/")
        assert resp.status_code == 500


def test_output_dict_is_transformed_to_response(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": 200}

    apigateway_mock.add_integration(
        "/", handler=handler, method="GET", endpoint="https://some/"
    )

    with httpx.Client() as client:
        resp = client.get("https://some/")
        assert resp.status_code == 200
