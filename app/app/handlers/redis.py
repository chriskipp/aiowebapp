# redis.py

import aiohttp_jinja2

from .base import BaseHandler


class RedisHandler(BaseHandler):
    async def info(self, request):

        pool = request.app["redis"]
        info = await pool.execute_command("INFO")
        #sections = info.split("\r\n\r\n")
        #parsed_sections = []
        #for section in sections:
        #    title = section.splitlines()[0][2:]
        #    rows = [
        #        [
        #            row.split(":")[0].replace("_", " ").title(),
        #            row.split(":")[1],
        #        ]
        #        for row in section.splitlines()[1:]
        #    ]
        #    parsed_sections.append({"title": title, "rows": rows})
        parsed_sections = [{"title": 'blub', "rows": [[str(k), str(v)] for k, v in info.items()]}]

        response = aiohttp_jinja2.render_template(
            "table.html",
            request,
            context={
                "pageheader": "Redis Stats",
                "sections": parsed_sections,
                "username": request["user"],
                "sidebar": self.sidebar_sections_loggedout,
            },
        )
        return response

    def configure(self, app):
        router = app.router
        router.add_route("GET", "/redis", self.info, name="redisinfo")
