import httpx

from pytest_aws_apigateway import ApiGateway


def test_handler(apigateway: ApiGateway):
    def handler(event, context):
        return httpx.Response(200, json={"body": "hello"})

    apigateway.add_integration(
        "/", handler=handler, method="GET", endpoint="https://some/"
    )

    with httpx.Client() as client:
        resp = client.get("https://some/")
        assert resp.json() == {"body": "hello"}
