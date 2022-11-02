#!/usr/bin/env python3

import secure

secure_headers = secure.Secure()


def setup_middlewares(app):

    # secure_headers middleware
    @app.middleware("response")
    async def set_secure_headers(request, response):
        secure_headers.framework.sanic(response)
