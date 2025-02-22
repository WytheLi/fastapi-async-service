import json
from aiokafka import AIOKafkaProducer

from loguru import logger
from settings import settings


class KafkaProducer:
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None  # 延迟初始化

    async def start(self):
        if self.producer is None:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            await self.producer.start()
            logger.info("Kafka Producer started.")

    async def send_message(self, topic: str, message: dict):
        if self.producer is None:
            raise RuntimeError("KafkaProducer has not been started")
        await self.producer.send(topic, message)

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka Producer stopped.")


kafka_producer = KafkaProducer(settings.KAFKA_BOOTSTRAP_SERVERS)
