#!/usr/bin/env python3

"""This module defines the index handler."""


async def slickgrid(request):  # pylint: disable=W0612
    """
    Route definition for /.

    Attributes:
      request (request): Reqest to handle.
    """
    return request.app.ctx.jinja.render(
            "slickgrid.html",
            request,
            sidebar=request.app.ctx.sidebar
    )

async def sql_editor(request):  # pylint: disable=W0612
    """
    Route definition for /.

    Attributes:
      request (request): Reqest to handle.
    """
    return request.app.ctx.jinja.render(
            "sql_editor.html",
            request,
            sidebar=request.app.ctx.sidebar
    )
