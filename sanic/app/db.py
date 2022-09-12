#!/usr/bin/env python3


def setup_database():

    import aiosqlite

    @app.listener("after_server_start")
    async def connect_to_db(*args, **kwargs):
        # app.ctx.db = await aiosqlite.connect('/var/sqlite/index.sqlite')
        app.ctx.db = await aiosqlite.connect("/var/sqlite/index.sqlite")
        await app.ctx.db.enable_load_extension(True)
        await app.ctx.db.load_extension("/var/sqlite/spellfix")

    @app.listener("after_server_stop")
    async def disconnect_from_db(*args, **kwargs):
        await app.ctx.db.close()
