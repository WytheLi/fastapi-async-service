import asyncio
import json
from aiokafka import AIOKafkaConsumer
from loguru import logger

from services.builders import BuilderFactory


class KafkaConsumer:
    def __init__(self, topic: str, bootstrap_servers: str, group_id: str):
        """Kafka 消费者封装，支持多种业务逻辑"""
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
        )
        self._task = None  # 任务引用

    async def start(self):
        """启动 Kafka 消费者"""
        await self.consumer.start()
        self._task = asyncio.create_task(self._consume_messages())

    async def _consume_messages(self):
        """异步消费 Kafka 消息，并分发到不同的业务逻辑"""
        async for msg in self.consumer:
            try:
                data = msg.value
                event_type = data.get("event_type")  # 解析消息类型
                logger.info(f"Received message: {data}")

                # 根据消息类型获取处理类并执行
                handler_cls = BuilderFactory.get_handler_cls(event_type)
                handler = handler_cls()
                await handler.handle(data["content"])  # 处理事件
            except Exception as e:
                logger.error(f"Error processing message: {e}")

    async def stop(self):
        """停止 Kafka 消费者"""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        await self.consumer.stop()
        logger.info("Kafka consumer stopped.")
