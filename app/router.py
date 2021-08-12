from fastapi import APIRouter

from app.routes import misc, redis, background

api_router = APIRouter()
api_router.include_router(misc.router, tags=["Misc"])
api_router.include_router(redis.router, prefix="/redis", tags=["Redis"])
api_router.include_router(background.router, prefix="/background", tags=["Background"])
