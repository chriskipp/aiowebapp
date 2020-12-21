import aiohttp_jinja2
import orjson
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


class LoginHandler:
    async def index(self, request):
        username = await authorized_userid(request)
        response = aiohttp_jinja2.render_template(
            "layout.html",
            request,
            context={"username": username, "sidebar": self.sidebar_sections},
        )
        return response

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
                    "sidebar": self.sidebar_sections,
                    "data": user,
                    "rows": user,
                },
            )
        else:
            raise web.HTTPFound("/login")

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
                    "sidebar": self.sidebar_sections,
                    "data": user,
                    "rows": user,
                },
            )
            return web.Response(text=str(user))
        else:
            return web.HTTPFound("/login")

    async def loginForm(self, request):
        username = await authorized_userid(request)
        response = aiohttp_jinja2.render_template(
            "login.html",
            request,
            context={"username": username, "sidebar": self.sidebar_sections},
        )
        return response

    async def login(self, request):
        session = await new_session(request)
        response = web.HTTPFound("/users/me")
        form = await request.post()
        login = form.get("loginField")
        password = form.get("passwordField")
        db_engine = request.app["dbsa"]
        if await check_credentials(db_engine, login, password):
            await remember(request, response, login)
            raise response

        raise web.HTTPFound("/login")

    async def logout(self, request):
        session = await get_session(request)
        await check_authorized(request)
        response = aiohttp_jinja2.render_template(
            "logout.html",
            request,
            context={"username": None, "sidebar": self.sidebar_sections},
        )
        await forget(request, response)
        session.invalidate()
        return response

        raise web.HTTPFound("/")

    async def public_page(self, request):
        await check_permission(request, "public")
        response = web.Response(
            text="This page is visible for all registered users"
        )
        return response

    async def protected_page(self, request):
        await check_permission(request, "protected")
        response = web.Response(text="You are on protected page")
        return response

    def configure(self, app):
        with open(app["project_root"] + "/" + "storage/data/routes.json") as f:
            routes = orjson.loads(f.read())

        self.sidebar_sections = [
            {
                "title": "User",
                "links": [
                    r["data"] for r in routes if r["category"] == "User"
                ],
            }
        ]

        router = app.router
        router.add_route("GET", "/", self.index, name="index")
        router.add_route("GET", "/users/me", self.me, name="me")
        router.add_route("GET", r"/users/{uid:\d+}", self.user, name="user")
        router.add_route("GET", "/login", self.loginForm, name="loginForm")
        router.add_route("POST", "/login", self.login, name="login")
        router.add_route("GET", "/logout", self.logout, name="logout")
        router.add_route("GET", "/public", self.public_page, name="public")
        router.add_route(
            "GET", "/protected", self.protected_page, name="protected"
        )
