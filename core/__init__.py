import os

from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from core.events import startup_handler, shutdown_handler
from core.exception_handler import http_exception_handler
from core.middleware.encryption import EncryptionMiddleware
from core.middleware.locale import LocaleMiddleware
from core.translation import translation_manager
from routers import api_router, direct_router
from settings import settings


def create_app() -> FastAPI:
    """FastAPI api controller"""
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL
    )

    # 添加 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS
    )
    # 添加i18n国际化中间件
    app.add_middleware(LocaleMiddleware, translation_manager=translation_manager)
    # API加密/解密
    app.add_middleware(EncryptionMiddleware)

    # 添加路由
    app.include_router(api_router, prefix=settings.API_PREFIX)
    app.include_router(direct_router)

    # 添加启动和关闭事件处理
    app.add_event_handler("startup", startup_handler(app))
    app.add_event_handler("shutdown", shutdown_handler(app))

    # 全局异常捕获，统一响应格式
    app.add_exception_handler(HTTPException, http_exception_handler)

    # 挂载静态文件目录
    static_dir = os.path.join(settings.BASE_PATH, "resources/static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    return app
