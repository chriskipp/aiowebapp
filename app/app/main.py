# main.py
import asyncio
import logging
import sys

from aiohttp import web
from aiohttp_security import setup as setup_security
from aiohttp_session import setup as setup_session

from app.db import setup_pg, teardown_pg, teardown_pgsa
from app.handlers import Login
from app.redis import setup_redis, teardown_redis
from app.session import setup_security, setup_session, teardown_session
from app.settings import get_config


def handler(request):
    return web.Response(text="Hello World!")


def create_app(loop, argv=None):
    app = web.Application(loop=loop)
    app["config"] = get_config(argv)

    # create db connection on startup, shutdown on exit
    app.on_startup.append(setup_redis)
    app.on_cleanup.append(teardown_redis)

    # create db connection on startup, shutdown on exit
    app.on_startup.append(setup_pg)
    app.on_cleanup.append(teardown_pg)

    # create SQLalchemy db connection on startup, shutdown on exit
    # app.on_startup.append(setup_pgsa)
    app.on_cleanup.append(teardown_pgsa)

    # create session on startup, shutdown on exit
    app.on_startup.append(setup_session)
    app.on_cleanup.append(teardown_session)

    # create SQLalchemy db connection on startup
    app.on_startup.append(setup_security)

    # app.router.add_get("/", handler)
    login_handler = Login()
    login_handler.configure(app)

    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app = create_app(loop)

    config = get_config(argv)

    web.run_app(app, host=app["config"]["host"], port=app["config"]["port"])


if __name__ == "__main__":
    main(sys.argv[-1:])
