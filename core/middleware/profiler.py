import os
import time

from pyinstrument import Profiler
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.responses import Response

from settings import settings


class PyInstrumentMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exclude_paths: list = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or ["/docs", "/redoc", "/openapi.json"]

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 排除指定路径
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # 通过URL参数`?profiler=true`激活分析，避免生产环境开销
        if request.query_params.get("profiler") != "true":
            return await call_next(request)

        # 初始化 Profiler（启用异步模式）
        profiler = Profiler(async_mode="enabled")
        profiler.start()

        response = await call_next(request)

        # 确保停止 Profiler 并生成报告
        profile_session = profiler.stop()
        html_report = profiler.output_html()

        path = request.url.path.replace("/", "_")[:100]

        if settings.PYINSTRUMENT_PROFILE_DIR:
            if not os.path.exists(settings.PYINSTRUMENT_PROFILE_DIR):
                os.makedirs(settings.PYINSTRUMENT_PROFILE_DIR, exist_ok=True)

            filename = "{total_time:.3f}s {path} {timestamp:.0f}.html".format(
                total_time=profile_session.duration,
                path=path,
                timestamp=time.time(),
            )

            file_path = os.path.join(settings.PYINSTRUMENT_PROFILE_DIR, filename)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_report)

            if request.method == "GET":
                return HTMLResponse(html_report)

        return response
