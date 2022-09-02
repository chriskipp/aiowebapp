#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic import Sanic

import aiosqlite

from environs import Env
from app.settings import Settings

from app.routes import setup_routes
from app.middlewares import setup_middlewares
from sanic_jinja2 import SanicJinja2
from sanic_session import InMemorySessionInterface


from sanic.response import redirect


app = Sanic(__name__.replace('.', '_'))

jinja = SanicJinja2(app, pkg_name='static')

session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)


def setup_database():

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        #app.ctx.db = await aiosqlite.connect('/var/sqlite/index.sqlite')
        app.ctx.db = await aiosqlite.connect('/var/sqlite/tmpfs/index.sqlite')
        await app.ctx.db.enable_load_extension(True)
        await app.ctx.db.load_extension('/var/sqlite/spellfix')

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        await app.ctx.db.close()


def init():
    env = Env()
    env.read_env()
    app.config.DB_URL =  env('DB_URL')

    app.config.load(Settings)
    setup_database()
    setup_routes(app)
    setup_middlewares(app)

    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
        auto_reload=True,
    )

