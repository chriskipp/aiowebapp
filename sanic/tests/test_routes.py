#!/usr/bin/env python3

import pytest
from sanic.response import json
from sanic_ext import serializer

#from app.main import create_app
from sanic import Sanic

FALLBACK_NAME = "app_main"
http_methods = [
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
    "PATCH",
    "TRACE",
]


@pytest.fixture
def app():
    from app.server import app

    #try:
    #    app = create_app()
    #except SanicException:
    #if True:
    #    app = Sanic.get_app(FALLBACK_NAME)

    @app.route("/.method_test", methods=http_methods)
    @serializer(json)
    async def do_action(request):
        return {"method": request.method}

    return app


@pytest.mark.asyncio
@pytest.mark.parametrize("method", http_methods)
async def test_methods(app, method):
    request, response = await app.asgi_client.request(method, "/.method_test")

    assert request.method.upper() == method
    if method.upper() == "HEAD":
        assert response.body == b""
    else:
        assert response.body == b'{"method":"' + f"{method}".encode() + b'"}'
    assert response.status == 200
