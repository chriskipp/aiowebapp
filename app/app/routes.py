# routes.py
import pathlib

import aiohttp_jinja2

from .handlers.mylogin import LoginHandler
from .handlers.redis import RedisHandler

# from .handlers.login import LoginHandler


PROJECT_ROOT = pathlib.Path(__file__).parent


def base_handler(request):
    response = aiohttp_jinja2.render_template("base.html", request, context=None)
    return response


def template_handler(request):
    response = aiohttp_jinja2.render_template("layout.html", request, context=None)
    return response


def setup_static_routes(app):
    app.router.add_static(
        "/static/", path=PROJECT_ROOT / "static", name="static", append_version=True
    )

    app.router.add_static(
        "/storage",
        path=PROJECT_ROOT / "storage",
        name="storage",
        show_index=True,
        append_version=False,
    )


def setup_routes(app):
    # app.router.add_get("/", index_handler)

    app.router.add_get("/base", base_handler)
    app.router.add_get("/template", template_handler)

    # Setup LoginHandler
    loginhandler = LoginHandler()
    loginhandler.configure(app)

    # Setup RedisHandler
    redishandler = RedisHandler()
    redishandler.configure(app)

    setup_static_routes(app)
