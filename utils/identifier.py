from typing import Union

from starlette.requests import Request
from starlette.websockets import WebSocket

from utils.signature import verify_token, get_authorization_header


async def custom_identifier(request: Union[Request, WebSocket]):
    """
    自定义限流器的key
    默认：fastapi-limiter:122.2.98.136:/api/v1/level/play:71:0
    :param request:
    :return:
    """
    token = await get_authorization_header(request)
    payload = await verify_token(token)
    return f'{payload["sub"]}:{request.scope["path"]}'
