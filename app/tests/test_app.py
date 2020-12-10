import asyncio
import logging

from aiohttp import web

from app.main import create_app


async def test_app_creation():
    app = create_app()
    app2 = web.Application()
    assert type(app) == type(app)


async def test_app_logger() -> None:
    app = create_app()
    assert type(app.logger) is logging.Logger
    assert app.logger.disabled == False


async def test_index(aiohttp_client):
    client = await aiohttp_client(create_app())
    resp = await client.get("/")
    assert resp.status == 200
