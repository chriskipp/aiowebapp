# search.py
import aiohttp_jinja2
from aiohttp import web
from redisearch import Client

from .base import BaseHandler

client = Client("manpages", host="redis", port=6379)


class SearchHandler(BaseHandler):
    async def search_get(self, request):
        response = aiohttp_jinja2.render_template(
            "search.html", request, context=await self.get_context(request, {})
        )
        return response

    async def autocomplete(self, request):
        pool = request.app["redis"]
        data = await request.post()
        res = await pool.execute(
            "FT.SUGGET",
            "cmp_manpages",
            data["q"],
            "MAX",
            "20",
            encoding="utf-8",
        )
        results = {"results": [{"id": i, "text": i} for i in res]}
        return web.json_response(results)

    async def search_post(self, request):
        pool = request.app["redis"]
        data = await request.post()
        res = await pool.execute(
            "FT.SEARCH",
            "manpages",
            '"' + data["q"].replace("-", " ") + '"',
            "WITHSCORES",
            "VERBATIM",
            "LIMIT",
            "0",
            "10",
            "HIGHLIGHT",
            "FIELDS",
            "1",
            "body",
            "TAGS",
            '''"<span class='highlight'>"''',
            '"</span>"',
            "SUMMARIZE",
            "FIELDS",
            "1",
            "body",
            encoding="utf-8",
        )
        results = {
            "total": res[0],
            "results": [
                {res[r][i]: res[r][i + 1] for i in range(0, len(res[r]), 2)}
                for r in range(3, len(res), 3)
            ],
        }
        for i in range(2, len(res), 3):
            results["results"][int((i - 2) / 3)]["score"] = res[i]

        return web.json_response(results)

    def configure(self, app):
        router = app.router
        router.add_route(
            "POST", "/autocomplete", self.autocomplete, name="autocomplete"
        )
        router.add_route("GET", "/search", self.search_get, name="search_get")
        router.add_route("POST", "/search", self.search_post, name="search")
