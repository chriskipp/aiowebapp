# main.py
import logging
import sys
import time

import aiohttp_debugtoolbar
import aiohttp_jinja2
import jinja2
import orjson
import uvloop
from aiohttp import web
from aiohttp_security import setup as setup_security
from aiohttp_session import get_session
from aiohttp_session import setup as setup_session

from app._dev.extra_pgsql import RequestPgDebugPanel
from app._dev.extra_redis import RequestRedisDebugPanel
from app.db import setup_pg, teardown_pg, teardown_pgsa
from app.middlewares import setup_middlewares
from app.redis import setup_redis, teardown_redis
from app.routes import setup_routes
from app.session import setup_security, setup_session, teardown_session
from app.settings import get_config


async def handler(request):
    return web.Response(text="Hello World!")


async def showsession(request):
    session = await get_session(request)
    session["age"] = time.time() - session.created
    text = (
        str(session.identity)
        + "\n"
        + orjson.dumps(
            {k: v for k, v in session.items()}, option=orjson.OPT_INDENT_2
        ).decode()
    )
    return web.Response(text=text)


def create_app(config=None):

    app = web.Application()
    app["config"] = get_config(config)

    # setup aiohttp-debugtoolbar
    aiohttp_debugtoolbar.setup(
        app,
        intercept_redirects=False,
        check_host=False,
        extra_templates="/usr/src/app/_dev/extra_tpl",
        extra_panels=[RequestPgDebugPanel, RequestRedisDebugPanel],
    )

    # setup Jinja2 template renderer
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("./app/templates/"))

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
    setup_middlewares(app)

    app.router.add_get("/", handler)
    app.router.add_get("/session", showsession)

    uvloop.install()
    setup_routes(app)

    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    config = None
    for i in range(len(argv)):
        if i in {"-c", "--config"}:
            config = argv[i + 1]

    app = create_app(config=config)

    web.run_app(app, host=app["config"]["host"], port=app["config"]["port"])


if __name__ == "__main__":
    main(sys.argv)
