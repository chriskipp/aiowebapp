#!/usr/bin/env python3

from sanic.response import json
from sanic.log import logger

def setup_routes(app):

    @app.get("/aurls")
    async def urls_list(request):
        query = """
        SELECT JSON_OBJECT(
          'fingerprint', fingerprint,
          'url', url,
          'title', title
        ) AS url
        FROM map
        ORDER BY fingerprint;
        --LIMIT 10;
        """
        async with app.ctx.db.execute(query) as cursor:
            records = await cursor.fetchall()
        logger.info(records)
        return json([record[0] for record in records])

    @app.route("/urls")
    async def urls_list(request):
        query = """
        SELECT JSON_OBJECT(
          'fingerprint', fingerprint,
          'url', url,
          'title', title
        ) AS url
        FROM map
        ORDER BY fingerprint;
        --LIMIT 10;
        """
        response = await request.respond()
        async with app.ctx.db.execute(query) as cursor:
            async for record in cursor:
                await response.send(record[0])

    @app.post("/complete")
    async def urls_list(request):
        query_completion = """
        SELECT word
          FROM spell
          WHERE word MATCH ?
            AND TOP=10;
        """
        q = request.json["q"]
        async with app.ctx.db.execute(query_completion, (q,)) as cursor:
            records = await cursor.fetchall()
        logger.info(records)
        return json([record[0] for record in records])
