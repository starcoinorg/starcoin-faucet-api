from typing import Optional
from aioredis import create_redis_pool, Redis
from loguru import logger
from app.core.config import settings


class RedisCache:

    def __init__(self):
        self.redis_cache: Optional[Redis] = None

    async def init_cache(self):
        logger.info("redis init start...")
        self.redis_cache = await create_redis_pool(settings.REDIS_DSN)
        logger.info("redis init finished")

    async def keys(self, pattern: str):
        return await self.redis_cache.keys(pattern)

    async def set(self, key: str, value: str, expire: int = 0):
        key = settings.REDIS_PREFIX + key
        return await self.redis_cache.set(key, value, expire=expire)

    async def get(self, key: str):
        key = settings.REDIS_PREFIX + key
        return await self.redis_cache.get(key)

    async def subscribe(self, channel: str):
        res = await self.redis_cache.subscribe(channel)
        return res

    async def publish(self, channel: str, message: str):
        return await self.redis_cache.publish(channel, message)

    async def close(self):
        logger.info("redis close start..")
        self.redis_cache.close()
        await self.redis_cache.wait_closed()
        logger.info("redis close finished")


redis_cache = RedisCache()
