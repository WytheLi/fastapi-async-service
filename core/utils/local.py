import uuid
from contextvars import ContextVar
from typing import Optional

from requests import Request

from settings import settings

# 定义上下文变量，用于存储当前请求
_request_var: ContextVar[Optional[Request]] = ContextVar("request", default=None)


def new_request_id() -> str:
    """生成一个新的唯一请求ID"""
    return uuid.uuid4().hex


class Local:
    """Global 访问当前请求及请求ID"""

    @property
    def request(self) -> Optional[Request]:
        return _request_var.get()

    @request.setter
    def request(self, value: Request) -> None:
        _request_var.set(value)

    @property
    def request_id(self) -> str:
        if self.request and hasattr(self.request, "request_id"):
            return getattr(self.request, "request_id")
        return new_request_id()

    def get_http_request_id(self) -> str:
        if not self.request:
            return new_request_id()

        # 从请求头中获取，没有的话新建一个
        request_id = self.request.headers.get(settings.HTTP_REQUEST_ID_HEADER, "")
        return request_id or new_request_id()

    def release(self) -> None:
        # 清理上下文变量
        _request_var.set(None)


local = Local()


def get_request_id():
    try:
        request_id = local.request.request_id
    except Exception:
        request_id = "NOT_CONTEXT"
    return request_id
