# main.py
import asyncio
import logging
import sys

from aiohttp import web

from app.settings import get_config


def handler(request):
    return web.Response(text="Hello World!")


def create_app(loop, argv=None):
    app = web.Application(loop=loop)
    app['config'] = get_config(argv)
    app.router.add_get("/", handler)
    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app = create_app(loop)

    config = get_config(argv)

    web.run_app(app, host=app['config']["host"], port=app['config']["port"])


if __name__ == "__main__":
    main(sys.argv[-1:])
