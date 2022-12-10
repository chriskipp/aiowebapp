#!/usr/bin/env python3

"""This module defines the index handler."""


async def index(request):  # pylint: disable=W0612
    """
    Route definition for /.

    Attributes:
      request (request): Reqest to handle.
    """
    return request.app.ctx.jinja.render(
        "index.html", request, sidebar=request.app.ctx.sidebar
    )
