from typing import Any, TypedDict, Union
import httpx
import re

PATH_PARAMETER_EXPRESSION = r"\{([^\/]+)\}"


class OutputFormatError(Exception): ...


def request_to_event(request: httpx.Request, resource: str) -> dict[str, Any]:
    # TODO isBase64Encoded depends on content-type header

    path = request.url.path
    path_parameters = _extract_path_parameters(path, resource)

    event = {
        "resource": resource,
        "path": request.url.path,
        "httpMethod": str(request.method),
        "headers": request.headers,
        "queryStringParameters": request.url.params,
        "body": request.content.decode(),
        "pathParameters": path_parameters,
    }
    return event


class OutputFormat(TypedDict):
    isBase64Encoded: bool
    statusCode: int
    headers: dict[str, str]
    multiValueHeaders: dict[str, list[str]]
    body: str


def transform_response(output: Union[dict[str, Any], httpx.Response]) -> httpx.Response:
    if isinstance(output, httpx.Response):
        return output
    if not isinstance(output, dict):
        raise ValueError
    if "statusCode" not in output:
        raise ValueError
    status_code = output["statusCode"]
    if not isinstance(status_code, int):
        raise OutputFormatError
    headers = output.get("headers")
    body = output.get("body")
    return httpx.Response(status_code=status_code, headers=headers, content=body)


def _extract_path_parameters(path: str, resource: str) -> Union[dict[str, str], None]:
    """Extract path parameters by comparing the URL path with the resource path.

    A resource like /orders/{id} has one path parameters `id`. By comparing with the actual path
    /orders/123 the function determines `id=123`.
    """
    p = re.compile(PATH_PARAMETER_EXPRESSION)

    def replacer(m: re.Match) -> str:
        name = m.groups()[0]
        stmt = f"(?P<{name}>[^\\/]+)"
        return stmt

    res = re.subn(p, replacer, resource)
    newp = re.compile(res[0])
    m = newp.match(path)
    path_parameters = m.groupdict() if m else None
    return path_parameters
