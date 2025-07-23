from typing import List

from fastapi import Depends
from fastapi.params import Header
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from core.exceptions import AuthorizationError
from core.exceptions import ForbiddenError
from core.exceptions import RequestException
from core.security import bearer_token_authentication
from db.async_engine import get_async_session
from services.repo.account import query_user_by_user_id
from settings import settings
from utils.signature import verify_token


def get_current_user(perms: List[str] = None):
    async def dependency(
        request: Request,
        session: AsyncSession = Depends(get_async_session),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_token_authentication),
    ):
        if credentials.scheme != settings.JWT_TOKEN_HEADER_PREFIX:
            raise AuthorizationError(message="Invalid authorization header")

        token = credentials.credentials
        payload = await verify_token(token)
        try:
            user_id = int(payload.get("sub"))
        except (TypeError, ValueError):
            raise AuthorizationError

        user = await query_user_by_user_id(session, user_id)
        if not user:
            raise ForbiddenError(message="Authentication failed")

        if perms:
            # 如果传入了权限参数，表示该接口需要指定权限才能访问，则验证用户是否有该权限
            user_roles = set(user.roles)
            has_permission = any(perms.name for role in user_roles for perms in role.perms)
            if not has_permission:
                raise ForbiddenError(message="Permission denied")
        return user

    return dependency


async def custom_http_headers(
    device_id: str = Header(None, alias="device_id", description="Device ID"),  # 使用alias强制解析device_id
    version: str = Header(None, description="App version"),
):
    # 检查必传公共参数
    if not all((device_id, version)):
        raise RequestException("Required parameters are missing")
    return {"device_id": device_id, "version": version}
