#!/usr/bin/env python3

import aioredis
import orjson


async def setup_redis(app):
    conf = app["config"]["redis"]
    adress = "redis://" + conf["host"] + ":" + str(conf["port"])
    pool = await aioredis.create_redis_pool(
        adress, minsize=conf["minsize"], maxsize=conf["maxsize"]
    )
    app["redis"] = pool

    return


async def teardown_redis(app):
    app["redis"].close()
    await app["redis"].wait_closed()


async def set_redis_key(pool, key, value):
    await pool.set(key, value)


async def get_redis_key(pool, key):
    return await pool.get(key, encoding="utf-8")


async def del_redis_key(pool, key):
    await pool.delete(key)


async def set_redis_json(pool, key, obj, path="."):
    await pool.execute("JSON.SET", key, path, orjson.dumps(obj))


async def get_redis_json(pool, key, path="."):
    return orjson.loads(await pool.execute("JSON.GET", key, path))
