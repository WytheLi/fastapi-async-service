import redis.asyncio as redis

from settings import settings


class RedisCache:
    """Redis 异步客户端封装"""

    def __init__(self, redis_url: str, decode_responses: bool = True):
        self.redis_url = redis_url
        self.decode_responses = decode_responses
        self.pool = None
        self.client = None

    async def connect(self):
        """初始化 Redis 连接池"""
        self.pool = redis.ConnectionPool.from_url(self.redis_url, decode_responses=self.decode_responses)
        self.client = redis.Redis(connection_pool=self.pool)

    async def close(self):
        """关闭 Redis 连接"""
        if self.pool:
            await self.pool.disconnect()

    def get_client(self) -> redis.Redis:
        """获取 Redis 客户端"""
        if not self.client:
            raise RuntimeError("Redis client is not initialized. Call `connect` first.")
        return self.client


cache = RedisCache(redis_url=settings.REDIS_URL)
