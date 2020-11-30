import asyncio
import logging

from aiohttp import web

from app.main import create_app

loop = asyncio.get_event_loop()


async def test_app_creation(loop=loop):
    app = create_app(loop)
    app2 = web.Application()
    assert type(app) == type(app)


async def test_app_logger(loop=loop) -> None:
    app = create_app(loop)
    assert type(app.logger) is logging.Logger
    assert app.logger.disabled == False


async def test_index(aiohttp_client):
    client = await aiohttp_client(create_app)
    resp = await client.get("/")
    assert resp.status == 200
