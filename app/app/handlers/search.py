# search.py
import aiohttp_jinja2
from aiohttp import web
from redisearch import Client, Query

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
        query = (
            Query(data["q"].replace("-", " "))
            .verbatim()
            .with_scores()
            .paging(0, 20)
            .highlight(tags=['<span class="highlight">', "</span>"])
            .summarize("body")
        )
        res = client.search(query)
        results = {
            "matches": res.total,
            "results": [
                {
                    "score": r.score,
                    "command": r.command,
                    "description": r.description,
                    "group": r.group,
                    "section": r.section,
                    "docpath": r.docpath,
                    "body": r.body,
                }
                for r in res.docs
            ],
        }
        return web.json_response(results)

    def configure(self, app):
        router = app.router
        router.add_route(
            "POST", "/autocomplete", self.autocomplete, name="autocomplete"
        )
        router.add_route("GET", "/search", self.search_get, name="search_get")
        router.add_route("POST", "/search", self.search_post, name="search")
