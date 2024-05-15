import httpx
import json
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response

from pytest_aws_apigateway import ApiGatewayMock


def test_resolver_implicit_response(apigateway_mock: ApiGatewayMock):
    app = APIGatewayRestResolver()

    @app.get("/orders/<id>")
    def list_orders(id: str):
        return {"id": id}

    apigateway_mock.add_integration(
        resource="/orders/{id}",
        method="GET",
        endpoint="http://localhost",
        handler=app.resolve,
    )

    with httpx.Client() as client:
        response = client.get("http://localhost/orders/123")
        assert response.json()["id"] == "123"


def test_resolver_response_object(apigateway_mock: ApiGatewayMock):
    app = APIGatewayRestResolver()

    @app.get("/orders/<id>")
    def list_orders(id: str):
        return Response(status_code=200, body=json.dumps({"id": id}))

    apigateway_mock.add_integration(
        resource="/orders/{id}",
        method="GET",
        endpoint="http://localhost",
        handler=app.resolve,
    )

    with httpx.Client() as client:
        response = client.get("http://localhost/orders/123")
        assert response.json()["id"] == "123"
