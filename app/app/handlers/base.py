import orjson


class BaseHandler:

    def __init__(self):
        sidebar_sections = ["User", "Tools"]

        with open("routes.json") as f:
            self.routes = orjson.loads(f.read())

        self.sidebar_sections_loggedin = [
            {
                "title": k["title"],
                "color": k["color"],
                "links": [
                    r["link"]
                    for r in k["data"]
                    if "logged_in" in r["requires"]
                ],
            }
            for k in self.routes
        ]

        self.sidebar_sections_loggedout = [
            {
                "title": k["title"],
                "color": k["color"],
                "links": [
                    r["link"]
                    for r in k["data"]
                    if "logged_out" in r["requires"]
                ],
            }
            for k in self.routes
        ]

    async def get_sidebar(self, request):
        if request["user"]:
            return self.sidebar_sections_loggedin
        else:
            return self.sidebar_sections_loggedout

    async def get_context(self, request, context):
        if request["user"]:
            context["username"] = request["user"]
        else:
            context["username"] = None
        context["sidebar"] = await self.get_sidebar(request)
        return context
