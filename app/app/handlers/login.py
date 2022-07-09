import time

import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import (check_authorized, check_permission, forget,
                              remember)
from aiohttp_session import new_session
from passlib.hash import sha256_crypt

from app.auth import check_credentials
from app.models import users

from .base import BaseHandler


class LoginHandler(BaseHandler):
    async def session(self, request):
        session = request["session"]
        session["age"] = time.time() - session.created
        return aiohttp_jinja2.render_template(
            "key_value_table.html",
            request,
            context={
                "username": request["user"],
                "heading": "Session",
                "rows": {k: v for k, v in session.items()},
                "sidebar": await self.get_sidebar(request),
            },
        )

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
                    "sidebar": await self.get_sidebar(request),
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
                    "sidebar": await self.get_sidebar(request),
                    "data": user,
                    "rows": user,
                },
            )
        else:
            raise web.HTTPUnauthorized()

    async def login_form(self, request):
        return aiohttp_jinja2.render_template(
            "login.html",
            request,
            context={
                "username": request["user"],
                "sidebar": await self.get_sidebar(request),
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
        session = request["session"]
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

    async def register_form(self, request):
        return aiohttp_jinja2.render_template(
            "register.html",
            request,
            context={
                "username": request["user"],
                "sidebar": await self.get_sidebar(request),
            },
        )

    async def register(self, request):
        form = await request.post()
        login = form.get("loginField")
        password = sha256_crypt.hash(form.get("passwordField"))
        db_engine = request.app["dbsa"]
        await check_permission(request, "register")
        insert = users.insert().values(login=login, passwd=password)
        async with db_engine.acquire() as conn:
            try:
                await conn.execute(insert)
                return web.Response(text="New User added!")
            except Exception as e:
                return web.Response(text=e.args[0])

    def configure(self, app):

        router = app.router
        router.add_route("GET", "/me", self.me, name="me")
        router.add_route("GET", "/session", self.session, name="session")
        router.add_route("GET", r"/users/{uid:\d+}", self.user, name="user")
        router.add_route("GET", "/login", self.login_form, name="loginForm")
        router.add_route("POST", "/login", self.login, name="login")
        router.add_route(
            "GET", "/users/register", self.register_form, name="registerForm"
        )
        router.add_route(
            "POST", "/users/register", self.register, name="register"
        )
        router.add_route("GET", "/logout", self.logout, name="logout")
