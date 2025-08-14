import asyncio

from loguru import logger


async def job():
    logger.info("Example task started.")
    await asyncio.sleep(1)
    logger.info("Example task finished.")
