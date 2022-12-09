#!/usr/bin/env python3

"""This module defines the leaflet handler."""

import ujson as json

async def leaflet(request):  # pylint: disable=W0612
    """
    Handler definition for map.

    Attributes:
      request (request): Reqest to handle.
    """
    return request.app.ctx.jinja.render(
            "leaflet.html",
            request,
            sidebar=request.app.ctx.sidebar
    )
