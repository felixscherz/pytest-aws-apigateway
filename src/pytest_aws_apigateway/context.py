from dataclasses import dataclass
from typing import Callable


@dataclass
class LambdaContext:
    aws_request_id: str
    log_stream_name: str
    invoked_function_arn: str
    client_context = None
    log_group_name: str
    function_name: str
    function_version: str
    memory_limit_in_mb: str
    identity = None


def create_context(handler: Callable) -> LambdaContext:
    name = handler.__name__
    return LambdaContext(
        aws_request_id="testing",
        log_stream_name=f"{name}-log-stream",
        log_group_name=f"{name}-log-group",
        invoked_function_arn=f"{name}",
        memory_limit_in_mb="128",
        function_version="$LATEST",
        function_name=f"{name}",
    )
