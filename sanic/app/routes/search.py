#!/usr/bin/env python3

"""This module defines the search and completion handlers."""

from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.log import logger

class CompletionView(HTTPMethodView):
    """
    Handler definitions for Completion view.
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
        logger.debug(request.form)
        if "q" in request.form:
            conn = request.app.ctx.sqlite
            cur = await conn.execute(
                    self.query,
                    (request.form["q"][0],)
            )
            data = await cur.fetchall()
            return json({
                "results": [
                    {
                        "id": r[0],
                        "text": r[0]
                    }
                    for r in data
                ]
            })
        return json({})

class SearchView(HTTPMethodView):
    """
    Handler definition for search.

    Attributes:
      request (request): Reqest to handle.
    """

    query = """
    SELECT-
        file AS title,
        dir || '/' || file AS docpath
      FROM fts_idx
      WHERE fts_idx
      MATCH ?
      ORDER BY bm25(fts_idx)
      LIMIT(10);
    """

    async def post(self, request):  # pylint: disable=W0612
        logger.debug(request.form)
        if "q" in request.form:
            conn = request.app.ctx.sqlite
            cur = await conn.execute(
                    self.query,
                    (request.form["q"][0],)
            )
            data = await cur.fetchall()
            return json([
                {
                  'title': r[0],
                  'docpath': r[1]
                }
                for r in data
            ])

    async def get(self, request):
        return request.app.ctx.jinja.render(
                "search.html",
                request,
                sidebar=request.app.ctx.sidebar
        )

