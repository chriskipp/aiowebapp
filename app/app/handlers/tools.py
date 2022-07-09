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

    async def plot(self, request):
        return aiohttp_jinja2.render_template(
            "line_plot.html",
            request,
            context=await self.get_context(request, {}),
        )

    async def tabs(self, request):
        return aiohttp_jinja2.render_template(
            "tabs.html",
            request,
            context=await self.get_context(request, {}),
        )

    async def chart(self, request):
        return aiohttp_jinja2.render_template(
            "chart.html",
            request,
            context=await self.get_context(request, {}),
        )

    async def charts(self, request):
        context = {}
        with open("forces/demo.html") as f:
            context["html"] = f.read()
        with open("forces/demo.css") as f:
            context["css"] = f.read()
        with open("forces/demo.js") as f:
            context["js"] = f.read()
        return aiohttp_jinja2.render_template(
            "charts.html",
            request,
            context=await self.get_context(request, context),
        )

    def configure(self, app):

        router = app.router
        router.add_route("GET", "/editor", self.editor, name="editor")
        router.add_route("GET", "/map", self.map, name="map")
        router.add_route("GET", "/nominatim", self.nominatim, name="nominatim")
        router.add_route("GET", "/tabs", self.tabs, name="tabs")
        router.add_route("GET", "/chart", self.chart, name="charts")
        router.add_route("GET", "/charts", self.chart, name="chart")
