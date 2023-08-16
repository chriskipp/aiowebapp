import aiopg.sa
import sqlalchemy as sa
import asyncpg


async def set_initial_search_path(conn):
    res = await conn.execute("SET search_path TO public,cron,urls")

async def setup_pg(app):
    conf = app["config"]["postgres"]
    pool = await asyncpg.create_pool(
        database=conf["database"],
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        min_size=conf["minsize"],
        max_size=conf["maxsize"],
        init=set_initial_search_path,
    )
    app["db"] = pool


async def teardown_pg(app):
    await app["db"].close()


async def execute_sql(query, pool):
    async with pool.acquire() as conn:
        async with conn.transaction():
            try:
                res = await conn.execute(query)
            except Exception as e:
                return e

    return res


async def fetch_sql(query, pool):
    async with pool.acquire() as conn:
        async with conn.transaction():
            try:
                res = await conn.fetch(query)
                res = [dict(r) for r in res]
            except Exception as e:
                return e

    # return ujson.dumps([dict(d) for d in res])
    return res


async def setup_pgsa(app):
    conf = app["config"]["postgres_sa"]
    engine = await aiopg.sa.create_engine(
        database=conf["database"],
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        minsize=conf["minsize"],
        maxsize=conf["maxsize"],
    )
    app["dbsa"] = engine


async def teardown_pgsa(app):
    app["dbsa"].close()
    await app["dbsa"].wait_closed()
