from textwrap import dedent

from aiohttp import web
from aiohttp_security import (
    authorized_userid,
    check_authorized,
    check_permission,
    forget,
    remember,
)

from app.auth import check_credentials


class Login(object):
    index_template = dedent(
        """<!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
                <p>{message}</p>
                <form action="/login" method="post">
                  Login:
                  <input type="text" name="login">
                  Password:
                  <input type="password" name="password">
                  <input type="submit" value="Login">
                </form>
                <a href="/logout">Logout</a>
            </body>
            </html>
    """
    )

    async def index(self, request):
        username = await authorized_userid(request)
        if username:
            template = self.index_template.format(
                message="Hello, {username}!".format(username=username)
            )
        else:
            template = self.index_template.format(message="You need to login")
        response = web.Response(body=template.encode(), content_type="text/html")
        return response

    async def login(self, request):
        response = web.HTTPFound("/")
        form = await request.post()
        login = form.get("login")
        password = form.get("password")
        db_engine = request.app["dbsa"]
        if await check_credentials(db_engine, login, password):
            await remember(request, response, login)
            raise response

        raise web.HTTPUnauthorized(text="Invalid username/password combination")

    async def logout(self, request):
        await check_authorized(request)
        response = web.Response(text="You have been logged out")
        await forget(request, response)
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
        router.add_route("GET", "/", self.index, name="index")
        router.add_route("POST", "/login", self.login, name="login")
        router.add_route("GET", "/logout", self.logout, name="logout")
        router.add_route("GET", "/public", self.internal_page, name="public")
        router.add_route("GET", "/protected", self.protected_page, name="protected")
