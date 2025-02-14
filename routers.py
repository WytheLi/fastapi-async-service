#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from api import account_router

direct_router = APIRouter()
api_router = APIRouter()

# direct_router.include_router(health_router, prefix='/health', tags=['服务健康探测'])

api_router.include_router(account_router, prefix='/auth', tags=['账号相关'])
