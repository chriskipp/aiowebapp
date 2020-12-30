import aiohttp_jinja2

from .base import BaseHandler


class ToolsHandler(BaseHandler):
    async def editor(self, request):
        return aiohttp_jinja2.render_template(
            "ace_editor.html",
            request,
            context=await self.get_context(request, {}),
        )

    def configure(self, app):

        router = app.router
        router.add_route("GET", "/editor", self.editor, name="editor")
