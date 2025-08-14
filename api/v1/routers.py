#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from api.v1.endpoints import account_router
from api.v1.endpoints import analysis_router
from api.v1.endpoints import health_router
from api.v1.endpoints import jobs_router
from api.v1.endpoints import message_router
from api.v1.endpoints import ws_router

direct_router = APIRouter()
api_router = APIRouter()

direct_router.include_router(health_router, prefix="/health", tags=["服务健康探测"])
direct_router.include_router(ws_router, prefix="/ws")
direct_router.include_router(jobs_router, prefix="/scheduler", tags=["scheduler"])

api_router.include_router(account_router, prefix="/auth", tags=["账号相关"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["分析数据"])
api_router.include_router(message_router, prefix="/message", tags=["messages"])
