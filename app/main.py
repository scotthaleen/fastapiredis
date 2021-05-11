# type: ignore[attr-defined]
import logging
from logging import Logger

from fastapi import FastAPI

from app.config import settings
from app.middleware import setup_middleware
from app.router import api_router

logger: Logger = logging.getLogger(__name__)

api = FastAPI(debug=True)
setup_middleware(api)
api.include_router(api_router, prefix=settings.API_V1_STR)


def print_debug_routes() -> None:
    max_len = max(len(route.path) for route in api.routes)
    routes = sorted(
        [(method, route.path, route.name) for route in api.routes for method in route.methods],
        key=lambda x: (x[1], x[0]),
    )
    route_table = "\n".join(f"{method:7} {path:{max_len}} {name}" for method, path, name in routes)
    logger.debug(f"Route Table:\n{route_table}")


@api.on_event("startup")
async def startup_event() -> None:
    logger.info("startup")
    logger.debug(settings)
    print_debug_routes()


@api.on_event("shutdown")
def shutdown_event() -> None:
    logger.debug("shutdown")
