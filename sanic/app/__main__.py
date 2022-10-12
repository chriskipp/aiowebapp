#!/usr/bin/env python3

from app.main import create_app


def run_app(app):
    app.run(
        host=app.config["HOST"],
        port=app.config["PORT"],
        workers=app.config["WORKERS"],
        debug=app.config["DEBUG"],
        access_log=app.config["ACCESS_LOG"],
    )


if __name__ == "__main__":
    app = create_app()
    run_app(app)
