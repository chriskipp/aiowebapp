#!/usr/bin/env python3

"""This module defines a handler for sanic-redis."""

import traceback

from sanic.log import logger
from sanic.response import json
from sanic.views import HTTPMethodView


class RedisView(HTTPMethodView):  # pylint: disable=W0612
    """Handler definitions for redis view."""

    async def post(self, request):
        """
        Handler definition for POST request.

        Attributes:
          request (request): Reqest to handle.
        """
        logger.debug(request.json)
        if "query" in request.json:
            async with request.app.ctx.redis as conn:
                try:
                    # res = await conn.fetch(request.json["query"])
                    res = await conn.execute_command("PING")
                    return json({"response": res})
                except BaseException:
                    exc = traceback.format_exc()
                    logger.error(exc)
                    return json([{"Error": exc}])
        return json([])

    async def get(self, request):
        """
        Handler definition for GET request.

        Attributes:
          request (request): Reqest to handle.
        """
        info = await request.app.ctx.redis.execute_command("INFO")
        return request.app.ctx.jinja.render(
            "redis_stats.html",
            request,
            pageheader="Redis Stats",
            sections=info,
            sidebar=request.app.ctx.sidebar,
        )
