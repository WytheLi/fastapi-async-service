#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from api import health_router
from settings import settings

direct_router = APIRouter()
api_router = APIRouter(prefix=settings.API_PREFIX)

direct_router.include_router(health_router, prefix='/health', tags=['服务健康探测'])
