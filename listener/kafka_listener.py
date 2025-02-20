import asyncio
import sys

from loguru import logger

from settings import settings
sys.path.insert(0, settings.BASE_PATH)

from infrastructure.kafka.consumer import KafkaConsumer


async def main():
    kafka_consumer = KafkaConsumer(
        topic=settings.KAFKA_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_GROUP_ID
    )

    await kafka_consumer.start()

    try:
        while True:
            await asyncio.sleep(1)  # 让主线程保持运行
    except KeyboardInterrupt:
        logger.info("Stopping consumer...")
        await kafka_consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
