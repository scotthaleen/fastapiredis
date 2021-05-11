from fastapi import APIRouter

from app.routes import misc, redis

api_router = APIRouter()
api_router.include_router(misc.router, tags=["Misc"])
api_router.include_router(redis.router, prefix="/redis", tags=["Redis"])
