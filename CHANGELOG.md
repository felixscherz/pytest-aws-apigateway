# pytest-aws-apigateway 0.5.1 (2024-05-16)

No significant changes.


# pytest-aws-apigateway 0.5.0 (2024-05-15)

### Features

- `add_integration` now accepts "ANY" as a http method as a catch-all
- `add_integration` now returns an `Integration` object with attributes for `resource`, `method` and `endpoint`


# pytest-aws-apigateway 0.4.1 (2024-05-14)

No significant changes.


# pytest-aws-apigateway 0.4.0 (2024-05-14)

No significant changes.


# pytest-aws-apigateway 0.3.0 (2024-05-13)

### Features

- Renamed fixture `apigateway` -> `apigateway_mock` and `ApiGateway` -> `ApiGatewayMock`


# pytest-aws-apigateway 0.2.0 (2024-05-13)

### Features

- Transform dictionary output to httpx.Response object


# pytest-aws-apigateway 0.1.0 (2024-05-10)

### Features

- Make `apigateway` available as a `pytest` fixture.
