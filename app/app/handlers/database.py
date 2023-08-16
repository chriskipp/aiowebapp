# database.py
import aiohttp_jinja2
import ujson
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
        res = ujson.dumps([dict(d) for d in response])
        return web.json_response(body=res)

    async def list_chart_links(self, request):
        query = """
        SELECT name FROM charts;
        """
        pool = request.app["db"]

        response = await fetch_sql(query, pool=pool)
        res = [d["name"] for d in response]
        # return web.json_response(body=res)
        return aiohttp_jinja2.render_template(
            "rendercharts.html", request, context={"charts": res}
        )

    async def render_chart(self, request):
        query = """
        SELECT * FROM charts
        WHERE name = '{}'
        ;
        """
        data = await request.post()
        chart = data["chart"]
        # print(data)
        pool = request.app["db"]

        response = await fetch_sql(query.format(chart), pool=pool)
        res = response[0]
        # return web.json_response(body=str(data))
        return aiohttp_jinja2.render_template(
            "charts.html", request, context=res
        )

    async def imprt(self, request):
        context = {}
        return aiohttp_jinja2.render_template(
            "import.html",
            request,
            context=await self.get_context(request, context),
        )

        res = ujson.dumps([dict(d) for d in response])
        return web.json_response(body=res)

    def configure(self, app):
        router = app.router
        router.add_route(
            "POST", "/database", self.handle_sql_query, name="sql_query"
        )
        router.add_route(
            "POST", "/renderchart", self.render_chart, name="render_chart"
        )
        router.add_route(
            "GET", "/database", self.sql_editor, name="sql_editor"
        )
        router.add_route(
            "GET",
            "/list_chart_links",
            self.list_chart_links,
            name="list_chart_links",
        )
        router.add_route(
            "GET",
            "/imprt",
            self.imprt,
            name="imprt"
        )
