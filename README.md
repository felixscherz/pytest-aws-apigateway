# pytest-aws-apigateway

[![PyPI - Version](https://img.shields.io/pypi/v/pytest-aws-apigateway.svg)](https://pypi.org/project/pytest-aws-apigateway)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-aws-apigateway.svg)](https://pypi.org/project/pytest-aws-apigateway)

-----

## Rationale

`pytest_aws_apigateway` is a pytest plugin to make testing AWS lambda integrations with API Gateway easier.


## Installation

```console
pip install pytest-aws-apigateway
```

## Usage

```python
def test_root_resource(apigateway_mock: ApiGatewayMock):
    def handler(event, context):
        return {"statusCode": 200, "body": json.dumps({"body": "hello"})}

    apigateway_mock.add_integration(
        "/", handler=handler, method="GET", endpoint="https://some/"
    )

    with httpx.Client() as client:
        resp = client.get("https://some/")
        assert resp.json() == {"body": "hello"}
```


## License

`pytest-aws-apigateway` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
