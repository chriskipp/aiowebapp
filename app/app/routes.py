# routes.py
import pathlib

# from .handlers import *

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    # app.router.add_get("/", index_handler)

    # app.router.add_get("/base", base_handler)
    # app.router.add_get("/layout", layout_handler)

    setup_static_routes(app)


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
