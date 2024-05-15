from httpx import Client

from pytest_aws_apigateway.integration import build_integration_request


def test_parse_path_parameters():
    client = Client()

    url = "https://some-path/my/path?a=True"
    resource = "/{id}/{id2}"
    req = client.build_request(url=url, method="GET")
    event = build_integration_request(req, resource=resource)
    assert event["pathParameters"]
    assert event["pathParameters"] == {"id": "my", "id2": "path"}
