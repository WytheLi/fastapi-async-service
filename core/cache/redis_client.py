import redis
from loguru import logger
from redis import RedisError

from settings import settings


class RedisClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance._init_redis()
        return cls._instance

    def _init_redis(self):
        try:
            self.pool = redis.ConnectionPool.from_url(settings.REDIS_URL, max_connections=20)
            self.client = redis.Redis(connection_pool=self.pool)
            logger.info("Redis client initialized successfully.")
        except RedisError as e:
            logger.error(f"Failed to initialize Redis client: {e}")
            raise e

    def get_client(self):
        return self.client

    def close(self):
        if self.pool:
            self.pool.disconnect()
            logger.info("Redis connection pool closed.")
