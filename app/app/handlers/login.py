import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import (
    authorized_userid,
    check_authorized,
    check_permission,
    forget,
    remember,
)
from aiohttp_session import get_session, new_session

from app.auth import check_credentials
from app.models import users

routes = [
    {
        "data": {
            "href": "/users/me",
            "icon": "fa-address-card",
            "label": "Profile",
        },
        "requires": ["logged_in"],
        "category": "User",
    },
    {
        "data": {"href": "/login", "icon": "fa-sign-in-alt", "label": "Login"},
        "requires": ["logged_out"],
        "category": "User",
    },
    {
        "data": {
            "href": "/logout",
            "icon": "fa-sign-out-alt",
            "label": "Logout",
        },
        "requires": ["logged_in"],
        "category": "User",
    },
]


class LoginHandler:
    async def me(self, request):
        username = await authorized_userid(request)
        if username:
            await check_authorized(request)

            async with request.app["dbsa"].acquire() as conn:
                query = users.select().where(users.c.login == username)
                ret = await conn.execute(query)
                values = await ret.fetchone()
            user = dict(values)
            user["passwd"] = "***"
            return aiohttp_jinja2.render_template(
                "user.html",
                request,
                context={
                    "username": username,
                    "sidebar": self.sidebar_sections_loggedin,
                    "data": user,
                    "rows": user,
                },
            )
        else:
            raise web.HTTPUnauthorized()

    async def user(self, request):
        username = await authorized_userid(request)
        if username:
            await check_authorized(request)
            query_uid = request.match_info["uid"]

            async with request.app["dbsa"].acquire() as conn:
                query = users.select().where(users.c.id == query_uid)
                ret = await conn.execute(query)
                values = await ret.fetchone()
            user = dict(values)
            user["passwd"] = "***"
            return aiohttp_jinja2.render_template(
                "user.html",
                request,
                context={
                    "username": username,
                    "sidebar": self.sidebar_sections_loggedin,
                    "data": user,
                    "rows": user,
                },
            )
        else:
            raise web.HTTPUnauthorized()

    async def login_form(self, request):
        username = await authorized_userid(request)
        return aiohttp_jinja2.render_template(
            "login.html",
            request,
            context={
                "username": username,
                "sidebar": self.sidebar_sections_loggedout,
            },
        )

    async def login(self, request):
        await new_session(request)
        response = web.HTTPFound("/users/me")
        form = await request.post()
        login = form.get("loginField")
        password = form.get("passwordField")
        db_engine = request.app["dbsa"]
        if await check_credentials(db_engine, login, password):
            await remember(request, response, login)
            raise response

        raise web.HTTPUnauthorized(
            text="Invalid username/password combination"
        )

    async def logout(self, request):
        session = await get_session(request)
        response = aiohttp_jinja2.render_template(
            "logout.html",
            request,
            context={
                "username": None,
                "sidebar": self.sidebar_sections_loggedout,
            },
        )
        await check_authorized(request)
        await forget(request, response)
        session.invalidate()
        return response

    async def public_page(self, request):
        await check_permission(request, "public")
        return web.Response(
            text="This page is visible for all registered users"
        )

    async def protected_page(self, request):
        await check_permission(request, "protected")
        return web.Response(text="You are on protected page")

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
        router.add_route("GET", "/users/me", self.me, name="me")
        router.add_route("GET", r"/users/{uid:\d+}", self.user, name="user")
        router.add_route("GET", "/login", self.login_form, name="loginForm")
        router.add_route("POST", "/login", self.login, name="login")
        router.add_route("GET", "/logout", self.logout, name="logout")
        router.add_route("GET", "/public", self.public_page, name="public")
        router.add_route(
            "GET", "/protected", self.protected_page, name="protected"
        )
