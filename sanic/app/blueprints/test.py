#!/usr/bin/env python3

from sanic.response import text
from sanic import Blueprint

from sanic_ext import serializer

bp_test = Blueprint("test", url_prefix="/test")


@bp_test.get("/")
@serializer(text)
async def test_handler(request):
    return "succsess!"
