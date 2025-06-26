from typing import Callable

from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp

from core.utils.translation import activate_translation
from core.utils.translation import deactivate_translation
from settings import settings


class LocaleMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable):
        # 从请求头中获取语言信息
        language = request.headers.get("Accept-Language", settings.LANGUAGE_CODE)
        request.state.language = language

        # 激活当前请求会话的翻译器
        activate_translation(language)

        # 从请求头中获取时区信息
        user_timezone = request.headers.get("X-Timezone", settings.TIME_ZONE)
        request.state.user_timezone = user_timezone

        response = await call_next(request)

        response.headers["X-User-Timezone"] = user_timezone

        response.background = BackgroundTask(self.at_last_execute)
        return response

    async def at_last_execute(self):
        # 请求结束后重置翻译器
        deactivate_translation()
