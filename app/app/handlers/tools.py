import aiohttp_jinja2

from .base import BaseHandler


class ToolsHandler(BaseHandler):
    async def editor(self, request):
        return aiohttp_jinja2.render_template(
            "ace_editor.html",
            request,
            context=await self.get_context(request, {}),
        )

    async def map(self, request):
        return aiohttp_jinja2.render_template(
            "leaflet.html",
            request,
            context=await self.get_context(request, {}),
        )

    async def nominatim(self, request):
        return aiohttp_jinja2.render_template(
            "nominatim.html",
            request,
            context=await self.get_context(request, {}),
        )

    async def slickgrid_tabs(self, request):
        return aiohttp_jinja2.render_template(
            "slickgrid.tabs.html",
            request,
            context=await self.get_context(request, {"xhruri": "https://localhost/storage/uploads/onlinetischreservierung.json"}),
        )

    async def tabs(self, request):
        tabsdata = [
            {"name": "editor", "content": markupsafe.Markup(template.render(elementId="editor"))}
        ]
        return aiohttp_jinja2.render_template(
            "tabs.html",
            request,
            context=await self.get_context(request, {"tabsdata": tabsdata}),
        )

    async def chart(self, request):
        return aiohttp_jinja2.render_template(
            "chart.html",
            request,
            context=await self.get_context(request, {}),
        )

    def configure(self, app):

        router = app.router
        router.add_route("GET", "/editor", self.editor, name="editor")
        router.add_route("GET", "/map", self.map, name="map")
        router.add_route("GET", "/nominatim", self.nominatim, name="nominatim")
        router.add_route("GET", "/tabs", self.tabs, name="tabs")
        router.add_route("GET", "/slickgrid_tabs", self.slickgrid_tabs, name="slickgrid_tabs")
        router.add_route("GET", "/chart", self.chart, name="charts")
