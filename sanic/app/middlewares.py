#!/usr/bin/env python3

import secure

secure_headers = secure.Secure()


def setup_middlewares(app):

    # secure_headers middleware
    @app.middleware("response")
    async def set_secure_headers(request, response):
        secure_headers.framework.sanic(response)

    # session middleware
    @app.middleware("request")
    async def add_session_to_request(request):
        # before each request initialize a session
        # using the client's request
        await session.open(request)


    # session middleware
    @app.middleware("response")
    async def save_session(request, response):
        # after each request save the session,
        # pass the response to set client cookies
        await session.save(request, response)


