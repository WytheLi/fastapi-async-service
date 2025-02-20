from typing import Callable

import redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from loguru import logger

from core.logger import configure_logger
from core.scheduler import scheduler_manager
from infrastructure.kafka.producer import kafka_producer
from settings import settings


def startup_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        logger.info("Fastapi service starting.")

        if settings.LOGFILE_OUTPUT:
            configure_logger()

        if not scheduler_manager.scheduler.running:
            scheduler_manager.start()

        # 初始化限流器
        redis_client = redis.asyncio.from_url(settings.REDIS_URL, decode_responses=True)
        await FastAPILimiter.init(redis_client)
        logger.info("FastAPILimiter Init.")

        # 启动 Kafka 生产者
        await kafka_producer.start()
        logger.info("Kafka Producer started.")
    return start_app


def shutdown_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        logger.info("Fastapi service shutdown.")

        scheduler_manager.shutdown()

        # 关闭 Kafka 生产者
        await kafka_producer.stop()
        logger.info("Kafka Producer stopped.")
    return stop_app
