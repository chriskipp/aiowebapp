import aiohttp_jinja2
from aiohttp_security import authorized_userid

routes = [
    {
        "data": {
            "href": "/users/me",
            "icon": "fa-address-card",
            "label": "Profile",
        },
        "requires": {"logged_in"},
        "category": "User",
    },
    {
        "data": {"href": "/login", "icon": "fa-sign-in-alt", "label": "Login"},
        "requires": {"logged_out"},
        "category": "User",
    },
    {
        "data": {
            "href": "/logout",
            "icon": "fa-sign-out-alt",
            "label": "Logout",
        },
        "requires": {"logged_in"},
        "category": "User",
    },
]


class BaseHandler:
    async def index(self, request):
        username = await authorized_userid(request)
        if username:
            return aiohttp_jinja2.render_template(
                "layout.html",
                request,
                context={
                    "username": username,
                    "sidebar": self.sidebar_sections_loggedin,
                },
            )
        else:
            return aiohttp_jinja2.render_template(
                "layout.html",
                request,
                context={
                    "username": None,
                    "sidebar": self.sidebar_sections_loggedout,
                },
            )

    def configure(self, app):

        self.sidebar_sections_loggedin = [
            {
                "title": "User",
                "links": [
                    r["data"]
                    for r in routes
                    if r["category"] == "User" and "logged_in" in r["requires"]
                ],
            }
        ]

        self.sidebar_sections_loggedout = [
            {
                "title": "User",
                "links": [
                    r["data"]
                    for r in routes
                    if r["category"] == "User"
                    and "logged_out" in r["requires"]
                ],
            }
        ]

        router = app.router
        router.add_route("GET", "/", self.index, name="index")
