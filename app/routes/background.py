import asyncio
import logging
import weakref
from logging import Logger
from typing import Any, Dict
from sse_starlette.sse import EventSourceResponse
from fastapi import APIRouter, BackgroundTasks, Request
import app.logging

logger: Logger = logging.getLogger(__name__)
qlogger: Logger = logging.getLogger("hello")

router = APIRouter()

Q = asyncio.Queue()
CLIENTS = weakref.WeakSet()

ping_rate = 30  # seconds

async def q_reader():
    global CLIENTS
    global Q
    logger.debug("** starting q reader **")
    while True:
        item = await app.logging.LOGQ.get()
        try:
            puts = [ch.put(item) for ch in CLIENTS]
            asyncio.gather(*puts)
        finally:
            app.logging.LOGQ.task_done()
            #Q.task_done()

def on_start():
    asyncio.create_task(q_reader())

async def emitter(msg):
    global Q
    await Q.put(msg)


async def events_client(request):
    global CLIENTS
    q = asyncio.Queue()
    CLIENTS.add(q)
    logger.debug("clients connected %s", len(CLIENTS))
    while True:
        if await request.is_disconnected():
            logger.debug('Request disconnected')
            break
        else:
            try:
                item = await q.get()
                yield {
                    "event": "data",
                    "data": item
                }
                q.task_done()
            except asyncio.exceptions.CancelledError:
                break

    logger.debug('a client disconnected')
    logger.debug("clients connected %s", len(CLIENTS) - 1)

async def background_work(data: str):
    logger.info(f"background {data}")
    qlogger.debug("custom")
    print(app.logging.LOGQ)
    await emitter(data)


@router.get("/msg/{data}", status_code=201)
async def start_task(data: str, back: BackgroundTasks) -> str:
    back.add_task(background_work, data)
    return "ok"


@router.get("/stream")
async def stream(request: Request):
    global ping_rate
    events = events_client(request)
    return EventSourceResponse(events, ping=ping_rate)
