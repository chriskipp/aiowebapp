#!/usr/bin/env python3

"""This module defines a handler for a asyncpg postgres handler."""

import traceback

from asyncpg.exceptions import PostgresSyntaxError
from sanic.log import logger
from sanic.response import json
from sanic.views import HTTPMethodView


class PostgresView(HTTPMethodView):  # pylint: disable=W0612
    """Handler definitions for Postgres view."""

    async def post(self, request):
        """
        Handler definition for POST request.

        Attributes:
          request (request): Reqest to handle.
        """
        logger.debug(request.json)
        if "query" in request.json:
            async with request.app.ctx.postgres.acquire() as conn:
                try:
                    res = await conn.fetch(request.json["query"])
                    res = [dict(row) for row in res]
                    return json(res)
                except PostgresSyntaxError:
                    exc = traceback.format_exc()
                    logger.error(exc)
                    return json([{"Error": exc}])
                except BaseException:
                    exc = traceback.format_exc()
                    logger.error(exc)
        return json([])

    async def get(self, request):
        """
        Handler definition for GET request.

        Attributes:
          request (request): Reqest to handle.
        """
        return request.app.ctx.jinja.render(
            "sql_editor.html", request, sidebar=request.app.ctx.sidebar
        )
