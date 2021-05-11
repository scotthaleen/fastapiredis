import logging
from logging import Logger
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger: Logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def read_root() -> str:
    logger.info("ok")
    return "ok"


@router.get("/echo/{s}")
async def echo(s: str) -> Dict[Any, Any]:
    return {"echo": s}


class Echo(BaseModel):
    s: str


@router.put("/echo")
async def echop(e: Echo) -> Dict[Any, Any]:
    return {"echo": e.s}


@router.get("/error")
async def read_error() -> Exception:
    try:
        raise Exception("test 500")
    except Exception:
        logger.exception("logged exception")
        raise HTTPException(status_code=500, detail="i am an exception")
