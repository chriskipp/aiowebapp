#!/usr/bin/env python3

import pytest

from app.main import create_app


@pytest.fixture
def app():
    sanic_app = create_app()
    return sanic_app


@pytest.mark.asyncio
async def test_basic_test_client(app):
    request, response = await app.asgi_client.get("/test")

    assert request.method.lower() == "get"
    assert response.body == b"succsess!"
    assert response.status == 200
