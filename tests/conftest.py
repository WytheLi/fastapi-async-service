from collections.abc import AsyncGenerator

import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport
from httpx import AsyncClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from core import create_app
from db import Base


@pytest_asyncio.fixture
async def async_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(name="client")
async def client_fixture(request) -> AsyncGenerator:
    app = create_app()

    # asgi_lifespan.LifespanManager 是用于管理 ASGI 应用生命周期事件（如启动和关闭）的工具
    # 作用：
    # 1. 触发生命周期事件：手动触发 ASGI 应用的 startup（启动）和 shutdown（关闭）事件，确保资源（如数据库连接、配置加载）正确初始化和清理。
    # 2. 异步上下文管理：提供异步上下文管理器（async with），简化生命周期事件的管理流程，自动处理异常和资源释放。
    # 3. 模拟服务器行为：在无 ASGI 服务器（如 Uvicorn）的环境中，模拟服务器对生命周期事件的处理，便于独立运行应用逻辑。
    # 在异步单元测试用例中，确保每个测试前后执行启动和关闭操作，避免资源泄漏或状态污染。
    async with (
        LifespanManager(app, startup_timeout=None, shutdown_timeout=None) as manager,
        AsyncClient(transport=ASGITransport(app=manager.app), base_url="http://testserver/", http2=True) as client,
    ):
        yield client
