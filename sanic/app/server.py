#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from db import connect_to_sqlite, disconnect_from_sqlite
from postgres import setup_pg, teardown_pg
from routes.db import query
from routes.postgres_handler import PostgresView
from routes.index import index
from routes.upload import upload
from routes.leaflet import leaflet
from routes.search import CompletionView, SearchView
from routes.slickgrid import slickgrid, sql_editor
from sanic_dropzone import Dropzone
from sanic_jinja2 import SanicJinja2
from sanic_session import InMemorySessionInterface, Session
import ujson as json

from sanic import Sanic

basedir = os.path.abspath(os.path.dirname(__file__))

app = Sanic(__name__)

app.config.update(
    HOST="0.0.0.0",
    PORT=8000,
    DEBUG=True,
    WORKERS=4,
    SECRET_KEY="dev key",  # the secret key used to generate CSRF token
    UPLOADED_PATH=os.path.join(basedir, "uploads"),
    UPLOAD_DIR=os.path.join(basedir, "uploads"),
    # Sanic-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE="image",
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=4096,
    FORWARDED_SECRET="YOUR SECRET",
    POSTGRES={
        "USER": 'postgres',
        "PASSWORD": 'password',
        "HOST": 'localhost',
        "PORT": 5432,
        "DATABASE": 'postgres',
        "MINSIZE": 3,
        "MAXSIZE": 30,
    }
)

# Serves files from the static folder to the URL /static
app.static("/static", "static")

session = Session(app, interface=InMemorySessionInterface())
app.ctx.jinja = SanicJinja2(app, session=session)

with open('routes.json') as f:
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
