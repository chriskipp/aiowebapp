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
from sanic_redis import SanicRedis  # pylint: disable=E0401
from sanic_session import InMemorySessionInterface, Session
from toml_config import TomlConfig
from sanic_jwt import Initialize
from sanic_jwt import exceptions
from sanic_jwt.decorators import protected
from sanic.response import json as jsonresponse


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


class User:

    def __init__(self, id, username, password):
        self.user_id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return "User(id='{}')".format(self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id, "username": self.username}


users = [User(1, "user1", "abcxyz"), User(2, "user2", "abcxyz")]

username_table = {u.username: u for u in users}
userid_table = {u.user_id: u for u in users}


async def authenticate(request, *args, **kwargs):
    #username = request.json.get("username", None)
    #password = request.json.get("password", None)
    username = request.form.get("loginField", None)
    password = request.form.get("passwordField", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user

async def retrieve_user(request, payload, *args, **kwargs):
    if payload:
        user_id = payload.get('user_id', None)
        #user = await User.get(user_id=user_id)
        #return user
        return {"user_id": user_id}
    else:
        return None

Initialize(
    app,
    authenticate=authenticate,
    cookie_set=True,
    #cookie_split=True,
    #refresh_token_enabled=True,
    #cookie_access_token_name='Auth',
    retrieve_user=retrieve_user,
    url_prefix='/auth',
    path_to_authenticate='/login',
    path_to_retrieve_user='/me',
    path_to_verify='/verify',
    path_to_refresh='/refresh',
)

@app.get('/auth/login')
async def login(request):
    return request.app.ctx.jinja.render(
        "login.html", request, sidebar=request.app.ctx.sidebar
    )

@app.get('/protected')
@protected()
async def protected(request):
    return jsonresponse({"verified": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
