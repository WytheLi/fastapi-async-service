from typing import Callable

import redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from loguru import logger

from core.cache.redis import cache
from core.logger import configure_logger
from core.scheduler import scheduler_manager
from infrastructure.kafka.producer import kafka_producer
from settings import settings


def startup_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        if settings.LOGFILE_OUTPUT:
            configure_logger()

        if not scheduler_manager.scheduler.running:
            scheduler_manager.start()

        # 初始化限流器
        redis_client = redis.asyncio.from_url(settings.REDIS_URL, decode_responses=True)
        await FastAPILimiter.init(redis_client)

        # 启动 Kafka 生产者
        if settings.KAFKA_BOOTSTRAP_SERVERS:
            await kafka_producer.start()

        # 初始化redis连接池
        await cache.connect()
    return start_app


def shutdown_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        scheduler_manager.shutdown()

        # 关闭 Kafka 生产者
        await kafka_producer.stop()

        # 关闭redis连接
        await cache.close()
    return stop_app
