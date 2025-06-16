import json
import time
from typing import Callable

from loguru import logger
from starlette.background import BackgroundTask
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.types import ASGIApp

from core.utils.local import get_request_id
from core.utils.local import local
from settings import settings


class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    请求上下文中间件

    request_id 全链路日志追踪使用
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()

        # 获取request_id
        request_id = local.get_http_request_id()
        request.request_id = request_id

        # 绑定当前请求
        local.request = request

        # 二进制类型文件请求体日志忽略
        if request.headers.get("content-type", "") != "multipart/form-data":
            raw_body = await request.body()
            if raw_body:
                try:
                    content = json.loads(raw_body)
                except Exception:
                    content = raw_body.decode("utf-8")

                # TODO 上线这里应该处理日志脱敏、请求体大小截断，我这里省略了
                logger.bind(request_id=get_request_id()).info(content)

        response = await call_next(request)

        # 在响应头中返回 request_id
        response.headers[settings.HTTP_REQUEST_ID_HEADER] = request_id

        process_time = time.time() - start_time
        # 添加处理时间到响应头
        response.headers[settings.HTTP_PROCESS_TIME_HEADER] = str(process_time)

        response.background = BackgroundTask(self.at_last_execute, request)
        return response

    async def at_last_execute(self, request: Request):
        """
        在响应完全发送后释放上下文（否则uvicorn日志获取request_id时候，local上下文已经释放，造成获取不到）
        """
        # 最后清理上下文
        local.release()
