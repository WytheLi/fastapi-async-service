from typing import Any

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


class StandardJSONResponse(JSONResponse):
    """
    Standard JSON Response that includes additional headers.

    Unified response format.
    """

    def __init__(self, code: int, msg: str = "success", data: Any = None, **kwargs):
        body = {"code": code, "message": msg}

        if data is not None:
            body.update({"data": data})

        # 使用 jsonable_encoder 将数据转换为可以序列化的格式
        content = jsonable_encoder(body)

        super().__init__(content=content, **kwargs)
