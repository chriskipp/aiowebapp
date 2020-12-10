import aiohttp_jinja2
from aiohttp import web
import orjson
import pathlib

from aiohttp_security import (
    authorized_userid,
    check_authorized,
    check_permission,
    forget,
    remember,
)
from aiohttp_session import get_session, new_session

from app.auth import check_credentials

class LoginHandler():

    async def index(self, request):
        username = await authorized_userid(request)
        response = aiohttp_jinja2.render_template(
            "layout.html", request, context={
                "username": username,
                "sidebar": self.sidebar_sections
            }
        )
        return response

    async def me(self, request):
        username = await authorized_userid(request)
        if username:
            return aiohttp_jinja2.render_template(
                "user.html", request, context={
                "username": username,
                "sidebar": self.sidebar_sections
                }
            )
        else:
            raise web.HTTPFound("/login")

#    async def user(self, request):
#        username = await authorized_userid(request)
#        if username:
#            await check_authorized(request)
#
#            async with request.app['dbsa'].acquire() as conn:
#                query = models.users.select().where(users.c.login == username)
#                ret = await conn.execute(query)
#            user = {k:v for k, v in zip(ret.keys(), await ret.fetchone())}
#            return aiohttp_jinja2.render_template('user.html', request,
#                    context={
#                        'username':username,
#                        "sidebar":self.sidebar_sections,
#                        "user": user
#                        })
#        else:
#            return web.HTTPFound("/login")



    async def loginForm(self, request):
        username = await authorized_userid(request)
        response = aiohttp_jinja2.render_template(
            "login.html", request, context={
                "username": username,
                "sidebar": self.sidebar_sections
            }
        )
        return response


    async def login(self, request):
        session = await new_session(request)
        response = web.HTTPFound("/me")
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
            "logout.html", request, context={
            "username": None,
            "sidebar": self.sidebar_sections
            }
        )
        await forget(request, response)
        session.invalidate()
        return response

        raise web.HTTPFound('/')

    def configure(self, app):
        with open(app['project_root'] + '/' + 'storage/data/routes.json') as f:
            routes = orjson.loads(f.read())

        self.sidebar_sections = [
          {
            "title": "User",
            "links": [r['data'] for r in routes if r['category'] == "User"]
          }
        ]

        router = app.router
        router.add_route("GET", "/", self.index, name="index")
        router.add_route("GET", "/me", self.me, name="me")
        router.add_route("GET", "/login", self.loginForm, name="loginForm")
        router.add_route("POST", "/login", self.login, name="login")
        router.add_route("GET", "/logout", self.logout, name="logout")
