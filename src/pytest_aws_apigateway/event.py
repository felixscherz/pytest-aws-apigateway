from typing import Any, Union
import httpx
import re


def request_to_event(request: httpx.Request, resource: str) -> dict[str, Any]:
    # TODO isBase64Encoded depends on content-type header

    path = request.url.path
    p = re.compile(r"\{([^\/]+)\}")

    def replacer(m: re.Match) -> str:
        name = m.groups()[0]
        stmt = f"(?P<{name}>[^\\/]+)"
        return stmt

    res = re.subn(p, replacer, resource)
    newp = re.compile(res[0])
    m = newp.match(path)
    path_parameters = m.groupdict() if m else None

    event = {
        "resource": resource,
        "path": str(request.url.path),
        "httpMethod": str(request.method),
        "headers": request.headers,
        "queryStringParameters": request.url.params,
        "body": request.content.decode(),
        "pathParameters": path_parameters,
    }
    ...
    return event


def transform_response(output: Union[dict[str, Any], httpx.Response]) -> httpx.Response:
    if isinstance(output, httpx.Response):
        return output
    raise NotImplementedError()
