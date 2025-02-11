from functools import wraps
from typing import List

from fastapi import HTTPException, status


def authorize_required(permissions: List[str] = None):
    """
    认证鉴权装饰器，标记需要进行JWT认证并且验证权限的路由。
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取请求对象
            request = args[0] if args else kwargs.get('request')
            # 提取 token 进行验证
            token = request.headers.get("Authorization")
            if token is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
            if token.startswith("Bearer "):
                token = token[7:]
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")

            # 验证 token
            payload = verify_token(token)

            # 如果传入了权限参数，则验证用户是否有该权限
            if permissions:
                user_roles = set(payload.roles)
                if not any(role in user_roles for role in permissions):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You do not have access to this resource"
                    )

            # 将用户信息存储在请求中，后续可以访问
            request.state.user = payload
            return await func(*args, **kwargs)

        return wrapper

    return decorator
