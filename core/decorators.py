from functools import wraps
from typing import List

from core.exceptions import RequestException, ForbiddenError
from services.repo.account import query_user_by_user_id
from utils.signature import get_authorization_header, verify_token


def authorize_required(perms: List[str] = None):
    """
    认证鉴权装饰器，标记需要进行JWT认证并且验证权限的路由。
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 获取视图函数参数
            request = args[0] if args else kwargs.get('request')
            session = args[1] if args else kwargs.get('session')

            # 必传公共参数
            device_id = request.headers.get('device_id')
            package_name = request.headers.get('package_name')
            version = request.headers.get('version')
            if not all([device_id, package_name, version]):
                raise RequestException("Required parameters are missing.")

            token = await get_authorization_header(request)

            payload = await verify_token(token)
            user_id = int(payload.get('sub'))

            user = await query_user_by_user_id(session, user_id)

            # 如果传入了权限参数，表示该接口需要指定权限才能访问，则验证用户是否有该权限
            # authorize_required、permission_validation，通常分开处理
            if perms:
                user_roles = set(user.roles)
                if not any(role in user_roles for role in perms):
                    raise ForbiddenError(message="You do not have access to this resource")

            # 将用户信息存储在请求中，后续视图可以访问
            request.state.user = user
            return await func(*args, **kwargs)
        return wrapper

    return decorator
