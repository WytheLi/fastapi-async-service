# -*- coding:utf-8 -*-
"""
FastAPI 框架服务 和 基础设施环境 的健康情况检查接口
"""
from datetime import datetime

import pytz
import requests
from fastapi import Depends, Request, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse, PlainTextResponse

from core.cache.redis_client import RedisClient
from db.async_engine import get_async_session
from schemas.health import LocaleTimeSchema
from settings import settings
from utils.response import CustomJSONResponse, General

health_router = APIRouter()


@health_router.get("/")
async def service_info(request: Request):
    return PlainTextResponse(f"{settings.DESCRIPTION} {settings.VERSION}")


@health_router.get("/ping_baidu")
async def ping_baidu(request: Request):
    _ = request.state.gettext

    response = requests.get('https://www.baidu.com')
    if response.status_code == 200:
        content = _("Baidu is accessible.")
    else:
        content = _("Baidu is not accessible.")
    return JSONResponse(content)


@health_router.get("/ping_google")
async def ping_google(request: Request):
    _ = request.state.gettext

    response = requests.get('https://www.google.com')
    if response.status_code == 200:
        content = _("Google is accessible.")
    else:
        content = _("Google is not accessible.")
    return JSONResponse(content)


@health_router.get('/network_info')
async def network_info(request: Request):
    """
    Checking Network Situation
    """
    response = requests.get('https://ipinfo.io/json')
    data = response.json()
    return JSONResponse(data)


@health_router.get('/db')
async def root_db(request: Request, session: AsyncSession = Depends(get_async_session)):
    # SQLDB数据库连接健康检查
    try:
        # 尝试进行异步数据库连接健康检查
        async_result = await session.execute("show DATABASES")
        for i in async_result:
            print(f"Async DB: {i}")
    except TypeError:
        # 如果捕获到TypeError，说明db是同步会话
        sync_result = session.execute("show DATABASES")
        sync_r = sync_result.fetchall()
        for i in sync_r:
            print(f"Sync DB: {i}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection failed.")

    return PlainTextResponse("Database connection is healthy.")


@health_router.get("/redis")
async def redis_health(request: Request):
    try:
        # ping redis
        redis_client = RedisClient().get_client()
        pong = redis_client.ping()
        if pong:
            return JSONResponse(content={"status": "ok", "message": "Redis is connected"})
        else:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Redis ping failed")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Redis connection error: {e}")


@health_router.get('/locale_time')
async def locale_time(request: Request):
    tz = pytz.timezone('Asia/Shanghai')
    locale_time = datetime.now()
    china_time = datetime.now(tz)
    data = LocaleTimeSchema(locale_time=locale_time, china_time=china_time)
    return CustomJSONResponse(General.Success, data=data)
