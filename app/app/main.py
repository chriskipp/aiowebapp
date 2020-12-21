# main.py
import pathlib

import aiohttp_debugtoolbar
import aiohttp_jinja2
import jinja2
from aiohttp import web

from app._dev.extra_pgsql import RequestPgDebugPanel
from app._dev.extra_redis import RequestRedisDebugPanel
from app.db import setup_pg, teardown_pg, teardown_pgsa
from app.middlewares import setup_middlewares
from app.redis import setup_redis, teardown_redis
from app.routes import setup_routes
from app.session import setup_security, setup_session, teardown_session
from app.settings import get_config


def create_app(config=None) -> web.Application:

    app = web.Application()
    app["config"] = get_config(config)

    app["project_root"] = pathlib.Path(__file__).parent.as_posix()

    # setup aiohttp-debugtoolbar
    aiohttp_debugtoolbar.setup(
        app,
        intercept_redirects=False,
        check_host=False,
        extra_templates="/usr/src/app/_dev/extra_tpl",
        extra_panels=[RequestPgDebugPanel, RequestRedisDebugPanel],
    )

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader("./app/templates/")
    )

    # create db connection on startup, shutdown on exit
    app.on_startup.append(setup_redis)
    app.on_cleanup.append(teardown_redis)

    # create db connection on startup, shutdown on exit
    app.on_startup.append(setup_pg)
    app.on_cleanup.append(teardown_pg)

    # shutdown SQLalchemy db connection on exit
    app.on_cleanup.append(teardown_pgsa)

    # create session on startup, shutdown on exit
    app.on_startup.append(setup_session)
    app.on_cleanup.append(teardown_session)

    # create security using SQLalchemy db connection on startup
    app.on_startup.append(setup_security)

    # setup middlewares
    app.on_startup.append(setup_middlewares)

    setup_routes(app)

    return app
