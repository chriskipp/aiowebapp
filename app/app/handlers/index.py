import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import check_permission

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

    async def public_page(self, request):
        await check_permission(request, "public")
        return web.Response(
            text="This page is visible for all registered users"
        )

    async def protected_page(self, request):
        await check_permission(request, "protected")
        return web.Response(text="You are on protected page")

    def configure(self, app):
        router = app.router
        router.add_route("GET", "/", self.index, name="index")
        router.add_route("GET", "/public", self.public_page, name="public")
        router.add_route(
            "GET", "/protected", self.protected_page, name="protected"
        )
