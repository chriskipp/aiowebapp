import aiohttp_jinja2
import orjson
from aiohttp import web
from aiohttp_security import (
    check_authorized,
    check_permission,
    forget,
    remember,
)
from aiohttp_session import get_session, new_session

from app.auth import check_credentials
from app.models import users


class LoginHandler:
    async def me(self, request):
        if request["user"]:

            async with request.app["dbsa"].acquire() as conn:
                query = users.select().where(users.c.login == request["user"])
                ret = await conn.execute(query)
                values = await ret.fetchone()

            user = dict(values)
            user["passwd"] = "************"
            return aiohttp_jinja2.render_template(
                "user.html",
                request,
                context={
                    "username": request["user"],
                    "sidebar": self.sidebar_sections_loggedin,
                    "data": user,
                    "rows": user,
                },
            )
        else:
            raise web.HTTPUnauthorized()

    async def user(self, request):
        if request["user"]:
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
                    "username": request["user"],
                    "sidebar": self.sidebar_sections_loggedin,
                    "data": user,
                    "rows": user,
                },
            )
        else:
            raise web.HTTPUnauthorized()

    async def login_form(self, request):
        if request["user"]:
            return aiohttp_jinja2.render_template(
                "login.html",
                request,
                context={
                    "username": request["user"],
                    "sidebar": self.sidebar_sections_loggedin,
                },
            )
        else:
            return aiohttp_jinja2.render_template(
                "login.html",
                request,
                context={
                    "sidebar": self.sidebar_sections_loggedout,
                },
            )

    async def login(self, request):
        await new_session(request)
        response = web.HTTPFound("/me")
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

        with open("routes.json") as f:
            routes = orjson.loads(f.read())

        self.sidebar_sections_loggedin = [
            {
                "title": k,
                "links": [
                    r["data"] for r in v if "logged_in" in r["requires"]
                ],
            }
            for k, v in routes.items()
        ]

        self.sidebar_sections_loggedout = [
            {
                "title": k,
                "links": [
                    r["data"] for r in v if "logged_out" in r["requires"]
                ],
            }
            for k, v in routes.items()
        ]

        router = app.router
        router.add_route("GET", "/me", self.me, name="me")
        router.add_route("GET", r"/users/{uid:\d+}", self.user, name="user")
        router.add_route("GET", "/login", self.login_form, name="loginForm")
        router.add_route("POST", "/login", self.login, name="login")
        router.add_route("GET", "/logout", self.logout, name="logout")
        router.add_route("GET", "/public", self.public_page, name="public")
        router.add_route(
            "GET", "/protected", self.protected_page, name="protected"
        )
