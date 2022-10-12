# redis.py

import aiohttp_jinja2

from .base import BaseHandler


class RedisHandler(BaseHandler):

    async def info(self, request):

        pool = request.app["redis"]
        info = await pool.execute_command("INFO")
        parsed_sections = [{"title": 'blub', "rows": [[str(k), str(v)] for k, v in info.items()]}]

        response = aiohttp_jinja2.render_template(
            "redis_stats.html",
            request,
            context={
                "pageheader": "Redis Stats",
                "sections": info,
                "username": request["user"],
                "sidebar": self.sidebar_sections_loggedout,
            },
        )
        return response

    def configure(self, app):
        router = app.router
        router.add_route("GET", "/redis", self.info, name="redisinfo")
