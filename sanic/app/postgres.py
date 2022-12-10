#!/usr/bin/env python3

"""
This module initializes and closes a connection to a postgresql database in.

the app ctx.
"""

import asyncpg
from sanic.log import logger


async def setup_pg(app):  # pylint: disable=W0612
    """
    Connects app to postgres database given in app config.

    Attributes:
      app (app): App to initialize connetion to.
    """
    conf = app.config["POSTGRES"]
    logger.info(conf)
    app.ctx.postgres = await asyncpg.create_pool(
        database=conf["DATABASE"],
        user=conf["USER"],
        password=conf["PASSWORD"],
        host=conf["HOST"],
        port=conf["PORT"],
        min_size=conf["MINSIZE"],
        max_size=conf["MAXSIZE"],
    )


async def teardown_pg(app):  # pylint: disable=W0612
    """
    Closes postgres database connection initialized with app.

    Attributes:
      app (app): App to close connection from.
    """
    await app.ctx.postgres.close()
