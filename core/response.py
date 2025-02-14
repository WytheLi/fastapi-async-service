from typing import Dict, Any

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


class CustomJSONResponse(JSONResponse):
    def __init__(self, general: Dict, data: Any = None, **kwargs):
        general.update({"data": data})

        # 使用 jsonable_encoder 将数据转换为可以序列化的格式
        content = jsonable_encoder(general)

        super().__init__(content=content, **kwargs)
