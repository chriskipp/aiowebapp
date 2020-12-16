# redis.py
import aiohttp_jinja2
from aiohttp import web

routes = web.RouteTableDef()


class RedisHandler:
    async def info(self, request):
        pool = request.app["redis"]
        info = await pool.execute("INFO", encoding="utf-8")
        sections = info.split("\r\n\r\n")
        parsed_sections = []
        for section in sections:
            title = section.splitlines()[0][2:]
            rows = [
                [row.split(":")[0].replace("_", " ").title(), row.split(":")[1]]
                for row in section.splitlines()[1:]
            ]
            parsed_sections.append({"title": title, "rows": rows})

        response = aiohttp_jinja2.render_template(
            "table.html",
            request,
            context={"pageheader": "Redis Live Stats", "sections": parsed_sections},
        )
        return response

    def configure(self, app):
        router = app.router
        router.add_route("GET", "/redis/info", self.info, name="redisinfo")