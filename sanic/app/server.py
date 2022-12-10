#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains the main file to run sanic.

Execute it by running:
    sanic server.app
"""

import os

import ujson as json
from db import connect_to_sqlite, disconnect_from_sqlite
from postgres import setup_pg, teardown_pg
from routes.db import query
from routes.index import index
from routes.leaflet import leaflet
from routes.postgres_handler import PostgresView
from routes.redis_handler import RedisView
from routes.search import CompletionView, SearchView
from routes.slickgrid import slickgrid, sql_editor
from routes.upload import upload
from sanic_dropzone import Dropzone
from sanic_jinja2 import SanicJinja2
from sanic_redis import SanicRedis
from sanic_session import InMemorySessionInterface, Session
from toml_config import TomlConfig

from sanic import Sanic

app = Sanic(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
config = TomlConfig(path=basedir + "/config/config.toml")

app.config.update(config)

# Serves files from the static folder to the URL /static
app.static("/static", "static")

session = Session(app, interface=InMemorySessionInterface())
app.ctx.jinja = SanicJinja2(app, session=session)

redis = SanicRedis(config_name="REDIS")
redis.init_app(app)

with open("routes.json", encoding="UTF-8") as f:
    app.ctx.sidebar = json.loads(f.read())

app.ctx.dropzone = Dropzone(app)

app.register_listener(connect_to_sqlite, "after_server_start")
app.register_listener(disconnect_from_sqlite, "before_server_stop")

app.register_listener(setup_pg, "after_server_start")
app.register_listener(teardown_pg, "before_server_stop")

app.add_route(index, "/", methods=["GET", "POST"])
app.add_route(upload, "/upload", methods=["GET", "POST"])
app.add_route(query, "/query", methods=["GET"])
app.add_route(leaflet, "/map", methods=["GET"])
app.add_route(slickgrid, "/slickgrid", methods=["GET"])
app.add_route(sql_editor, "/sql_editor", methods=["GET"])
app.add_route(SearchView.as_view(), "/search")
app.add_route(CompletionView.as_view(), "/completion")
app.add_route(PostgresView.as_view(), "/postgres")
app.add_route(RedisView.as_view(), "/redis")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
