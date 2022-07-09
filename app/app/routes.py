# routes.py
import pathlib

from aiohttp import web

from .handlers.database import DatabaseHandler
from .handlers.exchanger import DataHandler
from .handlers.index import IndexHandler
from .handlers.login import LoginHandler
from .handlers.redis import RedisHandler
from .handlers.search import SearchHandler
from .handlers.tools import ToolsHandler

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

    # Setup IndexHandler
    indexhandler = IndexHandler()
    indexhandler.configure(app)

    # Setup LoginHandler
    loginhandler = LoginHandler()
    loginhandler.configure(app)

    # Setup RedisHandler
    redishandler = RedisHandler()
    redishandler.configure(app)

    # Setup SearchHandler
    searchhandler = SearchHandler()
    searchhandler.configure(app)

    # Setup DatabaseHandler
    databasehandler = DatabaseHandler()
    databasehandler.configure(app)

    # Setup ToolsHandler
    toolshandler = ToolsHandler()
    toolshandler.configure(app)

    # Setup Exchangehandler
    exchangehandler = DataHandler()
    exchangehandler.configure(app)

    setup_static_routes(app)
