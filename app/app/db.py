import aiopg
import aiopg.sa

# aiopg


async def setup_pg(app):
    conf = app["config"]["postgres"]
    pool = await aiopg.create_pool(
        database=conf["database"],
        user=conf["user"],
        password=conf["password"],
        host=conf["host"],
        port=conf["port"],
        minsize=conf["minsize"],
        maxsize=conf["maxsize"],
    )
    app["db"] = pool


async def teardown_pg(app):
    app["db"].close()
    await app["db"].wait_closed()


async def execute_sql(query, pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                await cur.execute(query)
                if not cur.description:
                    return cur.query, cur.statusmessage
                keys = [c.name for c in cur.description]
                ret = []
                async for row in cur:
                    ret.append({k: v for k, v in zip(keys, row)})
            except Exception as e:
                return cur.query, e

    return ret


# aiopg[sa]


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
