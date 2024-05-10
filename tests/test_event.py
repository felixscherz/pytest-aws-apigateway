from httpx import Client

from pytest_aws_apigateway.event import request_to_event


def test_request():
    client = Client()
    url = "https://some-path/my/path?a=True"
    req = client.build_request(url=url, method="GET")
    print(req)
    print(req.url)
    print(req.url.path)
    print(req.url.params)
    print(req.url.raw_path)
    ...


def test_parse_path_parameters():
    client = Client()

    url = "https://some-path/my/path?a=True"
    resource = "/{id}/{id2}"
    req = client.build_request(url=url, method="GET")
    event = request_to_event(req, resource=resource)
    assert event["pathParameters"]
    assert event["pathParameters"] == {"id": "my", "id2": "path"}
