# database.py
import aiohttp_jinja2
import orjson
from aiohttp import web

from ..db import fetch_sql
from .base import BaseHandler


class DatabaseHandler(BaseHandler):
    async def sql_editor(self, request):
        return aiohttp_jinja2.render_template(
            "sql_editor.html",
            request,
            context=await self.get_context(request, {}),
        )

    async def handle_sql_query(self, request):
        data = await request.json()
        query = data["query"]
        pool = request.app["db"]

        response = await fetch_sql(query, pool=pool)
        res = orjson.dumps([dict(d) for d in response])
        return web.json_response(body=res)

    def configure(self, app):
        router = app.router
        router.add_route(
            "POST", "/database", self.handle_sql_query, name="sql_query"
        )
        router.add_route(
            "GET", "/database", self.sql_editor, name="sql_editor"
        )
