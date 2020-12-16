#!/usr/bin/env python3

import logging
import sys

import uvloop
from aiohttp import web

from app.main import create_app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    app = create_app(config=argv)

    uvloop.install()
    web.run_app(app, host=app["config"]["host"], port=app["config"]["port"])


if __name__ == "__main__":
    main(sys.argv[1:])
