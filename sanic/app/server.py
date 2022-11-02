#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from routes.upload import upload
from routes.index import index
from routes.db import query
from db import connect_to_sqlite, disconnect_from_sqlite
from sanic_dropzone import Dropzone
from sanic_jinja2 import SanicJinja2
from sanic_session import InMemorySessionInterface, Session
from sanic.response import json
from sanic.request import Request

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
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE="image",
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=4096,
    FORWARDED_SECRET="YOUR SECRET",
)

# Serves files from the static folder to the URL /static
app.static("/static", "static")

session = Session(app, interface=InMemorySessionInterface())
app.ctx.jinja = SanicJinja2(app, session=session)

app.ctx.dropzone = Dropzone(app)
app.register_listener(connect_to_sqlite, 'after_server_start')
app.register_listener(disconnect_from_sqlite, 'before_server_stop')



app.add_route(index, "/", methods=["GET", "POST"])
app.add_route(upload, "/upload", methods=["GET", "POST"])
app.add_route(query, "/query", methods=["GET"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
