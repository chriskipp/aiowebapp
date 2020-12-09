import asyncio
import pytest
from aiohttp.test_utils import TestClient, TestServer, loop_context
from aiohttp import request
from app.main import create_app

routes_nologin = [
        ("/", 200),
        ("/login", 200),
        ("/logout", 401),
        ("/session", 200),
        ("/public", 401),
        ("/protected", 401),
        ("/storage", 200)
]

@pytest.mark.parametrize("route,status", routes_nologin)
async def test_route_nologin(aiohttp_client, route, status):
    client = await aiohttp_client(create_app())
    res = await client.get(route)
    assert res.status == status
