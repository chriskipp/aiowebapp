# routes.py
import pathlib

from aiohttp import web

from .handlers.index import IndexHandler
from .handlers.login import LoginHandler

PROJECT_ROOT: pathlib.Path = pathlib.Path(__file__).parent


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

    # app.router.add_get("/session", showsession, name="session")

    # Setup IndexHandler
    indexhandler = IndexHandler()
    indexhandler.configure(app)

    # Setup LoginHandler
    loginhandler = LoginHandler()
    loginhandler.configure(app)

    setup_static_routes(app)
