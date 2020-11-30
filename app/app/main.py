# main.py
import asyncio
import logging
import sys

from aiohttp import web


def handler(request):
    return web.Response(text="Hello World!")


def create_app(loop, argv=None):
    app = web.Application(loop=loop)
    app.router.add_get("/", handler)
    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    loop = asyncio.get_event_loop()
    app = create_app(loop)

    # config = get_config(argv)
    config = {"host": "0.0.0.0", "port": 8080}

    web.run_app(app, host=config["host"], port=config["port"])


if __name__ == "__main__":
    main(sys.argv[-1:])
