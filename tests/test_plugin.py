import pytest


def test_fixture_is_available(pytester: pytest.Pytester):
    pytester.makepyfile(
        """
        import httpx

        import json
        from pytest_aws_apigateway import ApiGatewayMock


        def test_root_resource(apigateway_mock: ApiGatewayMock):
            def handler(event, context):
                return {"statusCode": 200, "body": json.dumps({"body": "hello"})}

            apigateway_mock.add_integration(
                "/", handler=handler, method="GET", endpoint="https://some/"
            )

            with httpx.Client() as client:
                resp = client.get("https://some/")
                assert resp.json() == {"body": "hello"}
        """
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
