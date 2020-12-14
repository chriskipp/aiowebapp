import aiohttp_jinja2

from .base import BaseHandler


class IndexHandler(BaseHandler):
    async def index(self, request):
        return aiohttp_jinja2.render_template(
            "layout.html",
            request,
            context={
                "username": request["user"],
                "sidebar": await self.get_sidebar(request),
            },
        )

    def configure(self, app):
        router = app.router
        router.add_route("GET", "/", self.index, name="index")
