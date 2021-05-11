import asyncio
import logging
from logging import Logger
from typing import Optional

import aioredis
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.config import settings

logger: Logger = logging.getLogger(__name__)
router = APIRouter()


class AsyncRedisPool:
    def __init__(self) -> None:
        self._pool: Optional[aioredis.Redis] = None
        self._lock = asyncio.Lock()

    async def __call__(self) -> aioredis.Redis:
        if self._pool is not None:
            return self._pool

        async with self._lock:
            if self._pool is not None:
                return self._pool
            logger.debug("Creating Redis Pool")
            host = settings.REDIS_HOST
            port = settings.REDIS_PORT
            pool = await aioredis.create_pool((host, port), encoding="utf-8")
            self._pool = aioredis.Redis(pool)
        return self._pool


redis_pool: aioredis.Redis = AsyncRedisPool()


class Item(BaseModel):
    ping: str


@router.get("/", response_model=Item)
async def ping_redis(redis: aioredis.Redis = Depends(redis_pool)) -> Item:
    logger.info("ping")
    return Item(ping=await redis.ping())
