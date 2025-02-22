from fastapi import Request, Response
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from core.crypto.aes import aes_encryption
from core.crypto.rsa import rsa_encryption
from settings import settings


class EncryptionMiddleware(BaseHTTPMiddleware):
    """API请求加密/解密中间件"""

    async def dispatch(self, request: Request, call_next):
        # 处理请求体（解密）
        if request.method in ["POST", "PUT", "PATCH"]:
            encrypted_body = await request.body()
            try:
                if settings.ENCRYPTION_ENABLED:
                    if settings.ENCRYPTION_TYPE == 'RSA':
                        decrypted_data = rsa_encryption.decrypt_with_private_key(encrypted_body.decode())
                    elif settings.ENCRYPTION_TYPE == 'AES':
                        decrypted_data = aes_encryption.decrypt(encrypted_body.decode())
                    else:
                        raise ValueError('Encryption type error.')
                    request._body = decrypted_data  # request._body必须是bytes类型才能被pydantic.BaseModel解析
            except Exception as e:
                # raise RequestException("Invalid encrypted request")
                ########################################################################################################
                # 为什么中间件的异常没有被捕获？
                # 1. FastAPI 的异常处理器 (app.add_exception_handler) 仅作用于路由处理逻辑，它只捕获视图函数（路由层）的异常。
                # 2. 中间件运行在请求生命周期的最外层，如果中间件内部发生异常，它不会进入 FastAPI 的异常处理逻辑，而是直接返回 500 错误。
                # 解决方案：在中间件里手动捕获异常，并返回标准响应
                ########################################################################################################
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"message": "Invalid encrypted request."}
                )

        response = await call_next(request)

        # 指定路由跳过加解密操作
        if request.url.path.startswith((settings.DOCS_URL, settings.REDOC_URL, settings.OPENAPI_URL)):
            response = await call_next(request)
            return response

        # 处理响应体（加密）
        if settings.ENCRYPTION_ENABLED and settings.ENCRYPTION_TYPE == 'AES':
            if response.headers.get("content-type") == "application/json":
                response_body = [chunk async for chunk in response.body_iterator]
                response_data = b"".join(response_body).decode()
                encrypted_response = aes_encryption.encrypt(response_data)
                return Response(content=encrypted_response, media_type="text/plain")
        return response
