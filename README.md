# pytest-aws-apigateway

[![PyPI - Version](https://img.shields.io/pypi/v/pytest-aws-apigateway.svg)](https://pypi.org/project/pytest-aws-apigateway)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-aws-apigateway.svg)](https://pypi.org/project/pytest-aws-apigateway)

-----

## Rationale

`pytest_aws_apigateway` is a pytest plugin to make testing AWS Lambda integrations with AWS ApiGateway easier.
It registers AWS Lambda function handlers as callbacks to requests made using `httpx` so you can test your
REST API using HTTP requests.

## Usage

### Add integrations

`pytest-aws-apigateway` lets you register AWS Lambda function handlers to act just like AWS ApiGateway proxy
integrations.

```python
import httpx
from pytest_aws_apigateway import ApiGatewayMock


def handler(event, context):
    return {"statusCode": 200, "body": json.dumps({"message": "Hello World!"})}

def test_hello_world(apigateway_mock: ApiGatewayMock):
    apigateway_mock.add_integration(
        "/", handler=handler, method="GET", endpoint="https://greetings/"
    )

    with httpx.Client() as client:
        resp = client.get("https://some/")
        assert resp.json() == {"message": "Hello World!"}
```


## License

`pytest-aws-apigateway` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
