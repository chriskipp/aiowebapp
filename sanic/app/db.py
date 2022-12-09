#!/usr/bin/env python3

"""
This module initializes and closes a connection to a sqlite3 database in.

the.

app ctx.
"""

import aiosqlite


# async def connect_to_sqlite(app, dbfile="/var/sqlite/index.sqlite", *args, **kwargs):
async def connect_to_sqlite(
    app, dbfile="index.sqlite"
):  # pylint: disable=W0612
    """
    Connects app to sqlite3 database given in dbfile.

    Attributes:
      app (app): App to initialize connetion to.
      dbfile (str): Path of the sqlite3 database file.
    """
    app.ctx.sqlite = await aiosqlite.connect(dbfile)
    await app.ctx.sqlite.enable_load_extension(True)
    await app.ctx.sqlite.load_extension("./spellfix")


async def disconnect_from_sqlite(app):  # pylint: disable=W0612
    """
    Closes sqlite3 connection initialized with app.

    Attributes:
      app (app): App to close connection from.
    """
    await app.ctx.sqlite.close()
