#!/usr/bin/env python3

"""This module defines the search and completion handlers."""

from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.log import logger

class PostgresView(HTTPMethodView):
    """
    Handler definitions for Postgres view.
    """

    query = """
    SELECT word
      FROM spell
      WHERE word MATCH ?
      ORDER BY rank DESC
      ;
    """

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
                except Exception:
                    exc = traceback.format_exc()
                    logger.error(exc)
                    return json([{"Error": exc}])
        return json([])

    async def get(self, request):
        return request.app.ctx.jinja.render(
                "sql_editor.html",
                request,
                sidebar=request.app.ctx.sidebar
        )

