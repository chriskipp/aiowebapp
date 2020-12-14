import orjson


class BaseHandler:
    def __init__(self):
        sidebar_sections = ["User", "Tools"]

        with open("routes.json") as f:
            self.routes = orjson.loads(f.read())

        self.sidebar_sections_loggedin = [
            {
                "title": k,
                "links": [
                    r["data"]
                    for r in self.routes[k]
                    if "logged_in" in r["requires"]
                ],
            }
            for k in sidebar_sections
        ]

        self.sidebar_sections_loggedout = [
            {
                "title": k,
                "links": [
                    r["data"]
                    for r in self.routes[k]
                    if "logged_out" in r["requires"]
                ],
            }
            for k in sidebar_sections
        ]

    async def get_sidebar(self, request):
        if request["user"]:
            return self.sidebar_sections_loggedin
        else:
            return self.sidebar_sections_loggedout
