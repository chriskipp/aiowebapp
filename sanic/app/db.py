#!/usr/bin/env python3


#def setup_sqlite(app):

import aiosqlite

#@app.listener("after_server_start")
async def connect_to_sqlite(app, *args, **kwargs):
    #app.ctx.sqlite = await aiosqlite.connect("/var/sqlite/index.sqlite")
    app.ctx.sqlite = await aiosqlite.connect("index.sqlite")
    await app.ctx.sqlite.enable_load_extension(True)
    #await app.ctx.sqlite.load_extension("/var/sqlite/spellfix")

#@app.listener("after_server_stop")
async def disconnect_from_sqlite(app, *args, **kwargs):
    await app.ctx.sqlite.close()


