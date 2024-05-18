from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from typing import Callable
from uuid import uuid4


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
    time = datetime.now(timezone.utc)
    return LambdaContext(
        aws_request_id=str(uuid4()),
        log_group_name=f"/aws/lambda/{name}",
        log_stream_name=f"{time:%Y}/{time:%m}/{time:%d}/[$LATEST]aws/lambda/{name}",
        invoked_function_arn=f"{name}",
        memory_limit_in_mb="128",
        function_version="$LATEST",
        function_name=f"arn:aws:lambda:us-east-1:123456789012:function:{name}",
    )
