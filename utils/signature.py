#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from typing import Union, Any

import jwt
from passlib.context import CryptContext
from starlette.requests import Request

from core.exceptions import AuthorizationError
from settings import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')  # 密码加密


def create_access_token(data: Union[int, Any], expires_delta: Union[timedelta, None] = None) -> str:
    """
    生成 jwt token

    :param data: 用户信息
    :param expires_delta: 增加的到期时间
    :return: 加密token
    """
    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(seconds=settings.JWT_TOKEN_EXPIRES)
    payload = {"exp": expires, "sub": str(data)}
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM).decode('utf-8')
    return f"{settings.JWT_TOKEN_HEADER_PREFIX} {token}"


async def verify_token(token: str) -> dict:
    """ JWT Token 解析和验证 """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            # options={"verify_exp": settings.JWT_TOKEN_EXPIRES},   # 当服务器有效期配置变更后，token会失效/重新激活
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthorizationError(message="Token has expired")
    except jwt.PyJWTError:
        raise AuthorizationError(message="Invalid token")


async def get_authorization_header(request: Request):
    token = request.headers.get("Authorization")
    if token is None:
        raise AuthorizationError(message="Authorization header missing")
    if token.startswith(settings.JWT_TOKEN_HEADER_PREFIX):
        token = token[7:]
    else:
        raise AuthorizationError(message="Invalid token format")
    return token
