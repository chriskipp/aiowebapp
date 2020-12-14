# routes.py
import pathlib
import time

import orjson
from aiohttp import web
from aiohttp_session import get_session

from .handlers.base import BaseHandler
from .handlers.login import LoginHandler

PROJECT_ROOT: pathlib.Path = pathlib.Path(__file__).parent


async def showsession(request: web.Request) -> web.Response:
    session = await get_session(request)
    session["age"] = time.time() - session.created
    text = (
        str(session.identity)
        + "\n"
        + orjson.dumps(
            {k: v for k, v in session.items()}, option=orjson.OPT_INDENT_2
        ).decode()
    )
    return web.Response(text=text)


def setup_static_routes(app: web.Application) -> None:
    app.router.add_static(
        "/static/",
        path=PROJECT_ROOT / "static",
        name="static",
        append_version=True,
    )

    app.router.add_static(
        "/storage",
        path=PROJECT_ROOT / "storage",
        name="storage",
        show_index=True,
        append_version=False,
    )


def setup_routes(app: web.Application) -> None:

    app.router.add_get("/session", showsession, name="session")

    # Setup BaseHandler
    basehandler = BaseHandler()
    basehandler.configure(app)

    # Setup LoginHandler
    loginhandler = LoginHandler()
    loginhandler.configure(app)

    setup_static_routes(app)
