#!/usr/bin/env python3

"""This module provides middlewares for the sanic app."""

import secure

secure_headers = secure.Secure()


def setup_middlewares(app):  # pylint: disable=W0612
    """
    Secure_headers middleware.

    Sets secure headers on returned responses.

    Attributes:
      app (app): App to be applied to.
    """

    @app.middleware("response")
    async def set_secure_headers(request, response):  # pylint: disable=W0613
        """Process response."""
        secure_headers.framework.sanic(response)
