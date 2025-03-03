#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from settings import settings


# 创建引擎（数据库连接的工厂，它还保留连接池内的连接以便快速重用）
async_engine = create_async_engine(
    settings.PGSQL_URL,
    echo=settings.DB_ECHO,
    future=True,
    pool_pre_ping=True
)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False  # 在提交后，访问对象时会重新从数据库加载数据/仍然使用缓存的对象数据
)


# async def create_table():
#     """
#     创建数据库表
#     """
#     from models import Base
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncSession:
    """
    with 管理上下文，显式调用 async_session
    """
    async with async_session() as session:
        try:
            yield session
        except Exception as ex:
            await session.rollback()
            raise ex
        else:
            await session.commit()
        finally:
            await session.close()


async def create_async_session():
    async with async_session() as session:
        return session


# @asynccontextmanager
# async def get_async_session() -> AsyncGenerator:
#     """
#     contextmanager自动管理上下文
#     """
#     async with async_session() as session:
#         try:
#             yield session
#         except Exception as ex:
#             await session.rollback()
#             raise ex
#         else:
#             await session.commit()
#         finally:
#             await session.close()
#
#
# async def get_db_session() -> AsyncSession:
#     async with get_async_session() as session:
#         yield session
