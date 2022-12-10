#!/usr/bin/env python3

"""This module defines the upload handler."""


async def query(request):  # pylint: disable=W0612
    """
    Handler to process a sqlite query.

    Attributes:
      request: Request to handle.
    """
    # if request.method == 'POST':
    if request.method == "GET":
        # if True:
        response = await request.respond()
        # q = request.parameters['q']
        q = "SELECT id FROM x;"
        async with request.app.ctx.sqlite.cursor() as curs:
            await curs.execute(q)
            async for record in curs:
                await response.send(str(record))
