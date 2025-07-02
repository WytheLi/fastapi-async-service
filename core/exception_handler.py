from fastapi import FastAPI
from fastapi.exceptions import ValidationException
from loguru import logger
from starlette import status
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


def add_exception_handler(app: FastAPI):

    @app.exception_handler(ValidationException)
    async def handle_request_validation_error(request: Request, exc: ValidationException):
        errors = []
        for error in exc.errors():
            loc = error["loc"]
            if len(loc) == 0:
                loc_part = "unknown_field"
            else:
                # 根据层级添加前缀（如 body.device_id）
                loc_part = ".".join(map(str, loc))
            msg = error["msg"]
            errors.append(f"{loc_part}: {msg}")

        logger.error(f"ValidationError: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Parameter error", "details": errors},
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": str(exc.detail)},
        )

    @app.exception_handler(Exception)
    async def handle_unhandled_exception(request: Request, exc: Exception):
        """
        处理其他未定义异常
        """
        logger.error(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "Internal server error"},
        )


async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # 处理 ValidationException（参数校验错误）
    if isinstance(exc, ValidationException):
        # errors = []
        # for error in exc.errors():
        #     loc = error["loc"]
        #     if len(loc) == 0:
        #         loc_part = "unknown_field"
        #     else:
        #         # 根据层级添加前缀（如 body.device_id）
        #         loc_part = ".".join(map(str, loc))
        #     msg = error["msg"]
        #     errors.append(f"{loc_part}: {msg}")

        logger.error(f"ValidationError: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Parameter error"},
        )
    # 处理 HTTPException
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": str(exc.detail)},
        )
    # 处理其他未定义异常
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal server error"},
    )
