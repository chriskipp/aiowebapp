#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.blueprints.test import bp_test
from app.toml_config import TomlConfig
from sanic import Sanic

# from app.routes import setup_routes
# from app.middlewares import setup_middlewares
# from sanic_jinja2 import SanicJinja2
# from sanic_session import InMemorySessionInterface

# jinja = SanicJinja2(app, pkg_name='static')

# session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)


def create_app():
    toml_config = TomlConfig(path="./config/dev.toml")
    app = Sanic(__name__.replace(".", "_"), config=toml_config)

    app.blueprint(bp_test)

    return app
