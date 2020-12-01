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


class Login(object):
    async def loginform(self, request):
        username = await authorized_userid(request)
        if username:
            response = aiohttp_jinja2.render_template(
                "login.html", request, context={"message": username}
            )
        else:
            response = aiohttp_jinja2.render_template(
                "login.html", request, context={"message": "Anonymous"}
            )
        return response

    async def login(self, request):
        session = await new_session(request)
        response = web.HTTPFound("/session")
        form = await request.post()
        login = form.get("login")
        password = form.get("password")
        db_engine = request.app["dbsa"]
        if await check_credentials(db_engine, login, password):
            await remember(request, response, login)
            raise response

        raise web.HTTPUnauthorized(text="Invalid username/password combination")

    async def logout(self, request):
        session = await get_session(request)
        await check_authorized(request)
        response = web.Response(text="You have been logged out")
        await forget(request, response)
        session.invalidate()
        return response

    async def internal_page(self, request):
        await check_permission(request, "public")
        response = web.Response(text="This page is visible for all registered users")
        return response

    async def protected_page(self, request):
        await check_permission(request, "protected")
        response = web.Response(text="You are on protected page")
        return response

    def configure(self, app):
        router = app.router
        router.add_route("GET", "/login", self.loginform, name="loginform")
        router.add_route("POST", "/login", self.login, name="login")
        router.add_route("GET", "/logout", self.logout, name="logout")
        router.add_route("GET", "/public", self.internal_page, name="public")
        router.add_route("GET", "/protected", self.protected_page, name="protected")
