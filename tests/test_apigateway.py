import json

import httpx

from pytest_aws_apigateway import ApiGatewayMock
from pytest_aws_apigateway import LambdaContext


def test_root_resource(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": 200, "body": json.dumps({"body": "hello"})}

    apigateway_mock.add_integration(
        "/", handler=handler, method="GET", endpoint="https://foo/"
    )

    with httpx.Client() as client:
        resp = client.get("https://foo/")
        assert resp.json() == {"body": "hello"}


def test_child_resource(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": 200, "body": json.dumps({"body": "hello"})}

    apigateway_mock.add_integration(
        "/orders", handler=handler, method="GET", endpoint="https://foo/"
    )

    with httpx.Client() as client:
        resp = client.get("https://foo/orders")
        assert resp.json() == {"body": "hello"}


def test_child_resource_with_parameter(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        params = event["pathParameters"]
        return {"statusCode": 200, "body": json.dumps({"params": params})}

    apigateway_mock.add_integration(
        "/orders/{id}", handler=handler, method="GET", endpoint="https://foo/"
    )

    with httpx.Client() as client:
        resp = client.get("https://foo/orders/123")
        assert resp.json() == {"params": {"id": "123"}}


def test_invalid_output_format_returns_500(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": "200"}

    apigateway_mock.add_integration(
        "/", handler=handler, method="GET", endpoint="https://foo/"
    )

    with httpx.Client() as client:
        resp = client.get("https://foo/")
        assert resp.status_code == 500


def test_output_dict_is_transformed_to_response(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": 200}

    apigateway_mock.add_integration(
        "/", handler=handler, method="GET", endpoint="https://foo/"
    )

    with httpx.Client() as client:
        resp = client.get("https://foo/")
        assert resp.status_code == 200


def test_match_on_ANY_method(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": 200, "body": json.dumps({"body": "hello"})}

    apigateway_mock.add_integration(
        "/", handler=handler, method="ANY", endpoint="https://foo/"
    )

    with httpx.Client() as client:
        resp = client.get("https://foo/")
        assert resp.json() == {"body": "hello"}


def test_headers_are_forwarded(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": 200, "body": json.dumps(event["headers"])}

    apigateway_mock.add_integration(
        "/", handler=handler, method="ANY", endpoint="https://foo/"
    )

    with httpx.Client() as client:
        resp = client.get("https://foo/", headers={"x-test": "testing"})
        assert resp.json()["x-test"] == "testing"


def test_query_strings_are_forwarded(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": 200, "body": json.dumps(event["queryStringParameters"])}

    apigateway_mock.add_integration(
        "/", handler=handler, method="ANY", endpoint="https://foo/"
    )

    with httpx.Client() as client:
        resp = client.get("https://foo/?testing&foo=bar")
        assert "testing" in resp.json()
        assert resp.json()["foo"] == "bar"


def test_custom_context_object_passed_to_handler(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": 200, "body": json.dumps({"body": context.function_name})}

    context = LambdaContext(
        aws_request_id="0773bb78-068f-43d6-b1d8-fe459da4de43",
        log_group_name="/aws/lambda/test-handler",
        log_stream_name="2024/05/15/[$LATEST]f54678254f1546a494246cf8ea130bc3",
        invoked_function_arn="arn:aws:lambda:us-east-1:123456789012:function:testApiGateway",
        function_name="test-handler",
        function_version="$LATEST",
        memory_limit_in_mb="128",
    )

    apigateway_mock.add_integration(
        "/", handler=handler, method="GET", endpoint="https://foo/", context=context
    )

    with httpx.Client() as client:
        resp = client.get("https://foo/")
        assert resp.json() == {"body": "test-handler"}


def test_custom_context_generator_passed_to_handler(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": 200, "body": json.dumps({"body": context.function_name})}

    def context():
        return LambdaContext(
            aws_request_id="0773bb78-068f-43d6-b1d8-fe459da4de43",
            log_group_name="/aws/lambda/test-handler",
            log_stream_name="2024/05/15/[$LATEST]f54678254f1546a494246cf8ea130bc3",
            invoked_function_arn="arn:aws:lambda:us-east-1:123456789012:function:testApiGateway",
            function_name="test-handler",
            function_version="$LATEST",
            memory_limit_in_mb="128",
        )

    apigateway_mock.add_integration(
        "/", handler=handler, method="GET", endpoint="https://foo/", context=context
    )

    with httpx.Client() as client:
        resp = client.get("https://foo/")
        assert resp.json() == {"body": "test-handler"}
