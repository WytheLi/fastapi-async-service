import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette_prometheus import PrometheusMiddleware
from starlette_prometheus import metrics

from core.events import shutdown_handler
from core.events import startup_handler
from core.exception_handler import add_exception_handler
from core.exception_handler import exception_handler
from core.middleware.context import RequestContextMiddleware
from core.middleware.encryption import EncryptionMiddleware
from core.middleware.locale import LocaleMiddleware
from core.middleware.profiler import PyInstrumentMiddleware
from core.translation import translation_manager
from routers import api_router
from routers import direct_router
from settings import settings


def create_app() -> FastAPI:
    """FastAPI api controller"""
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        openapi_url=settings.OPENAPI_URL,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
    )

    # 添加 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
        allow_methods=settings.ALLOW_METHODS,
        allow_headers=settings.ALLOW_HEADERS,
    )
    # 添加i18n国际化中间件
    app.add_middleware(LocaleMiddleware, translation_manager=translation_manager)
    # API加密/解密
    app.add_middleware(EncryptionMiddleware)
    # 添加 pyinstrument 性能分析中间件
    app.add_middleware(PyInstrumentMiddleware)
    # 添加 Prometheus 中间件
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", metrics)  # 暴露指标端点
    # 请求上下文中间件（该中间件需要放置在所有中间件的最末尾）
    app.add_middleware(RequestContextMiddleware)

    # if os.getenv("ENV") == "development":
    #     # Debug Toolbar
    #     app.add_middleware(
    #         DebugToolbarMiddleware,
    #         panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"]
    #     )

    # 添加路由
    app.include_router(api_router, prefix=settings.API_PREFIX)
    app.include_router(direct_router)

    # 添加启动和关闭事件处理
    app.add_event_handler("startup", startup_handler(app))
    app.add_event_handler("shutdown", shutdown_handler(app))

    # 全局异常捕获，统一响应格式（想要自定义响应格式，必须要手动注册异常处理函数到app，否则可能会被内置的异常处理函数处理）
    # app.add_exception_handler(HTTPException, exception_handler)
    # app.add_exception_handler(RequestValidationError, exception_handler)
    # app.add_exception_handler(Exception, exception_handler)
    add_exception_handler(app)

    # 挂载静态文件目录
    static_dir = os.path.join(settings.BASE_PATH, "resources/static")
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    return app
