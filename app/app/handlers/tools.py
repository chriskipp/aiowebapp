import aiohttp_jinja2

from .base import BaseHandler
from jinja2 import Template
import markupsafe

template = Template('''
  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.5/ace.js" type="text/javascript" charset="utf-8"></script>
  <!-- ace extentions -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.5/ext-language_tools.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.5/ext-modelist.js"></script>
  <div id="{{ elementId }}_editor" style="flex-flow:1;height:100%;width:100%;"></div>
  <script>
    function initEditor(elementId) {
      ace.require("ace/ext/language_tools");
      var editor = ace.edit(elementId);
      editor.session.setMode("ace/mode/sql");
      editor.setKeyboardHandler("ace/keyboard/vim");
      editor.setTheme("ace/theme/merbivore");
      editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: true
      });
    }
    //$(document.getElementById("tabList").children[0]).tab("show");
    initEditor("{{ elementId }}_editor");
  </script>
''')

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
