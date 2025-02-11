from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp

from core.translation import TranslationManager
from settings import settings


class LocaleMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, translation_manager: TranslationManager):
        super().__init__(app)
        self.translation_manager = translation_manager

    async def dispatch(self, request: Request, call_next: Callable):
        # 从请求头中获取语言信息
        language = request.headers.get('language', settings.LANGUAGE_CODE)
        request.state.language = language
        # 获取指定语言的翻译实例
        translation = self.translation_manager.get_translation(language)
        request.state.gettext = translation.gettext

        # 从请求头中获取时区信息
        user_timezone = request.headers.get('X-Timezone', settings.TIME_ZONE)

        response = await call_next(request)

        response.headers['X-User-Timezone'] = user_timezone
        return response
