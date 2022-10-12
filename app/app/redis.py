#!/usr/bin/env python3

import aioredis
import orjson


async def setup_redis(app):
    conf = app["config"]["redis"]
    adress = "redis://" + conf["host"] + ":" + str(conf["port"])
    pool = await aioredis.from_url(
        adress, encoding="utf-8", decode_responses=True
    )
    app["redis"] = pool

    return


async def teardown_redis(app):
    app["redis"].close()


async def set_redis_key(pool, key, value):
    await pool.execute_command("SET", key, orjson.dumps(value))


async def get_redis_key(pool, key):
    value = await pool.execute_command("GET", key)
    if value is not None:
        return orjson.loads(value)
    else:
        return value


async def del_redis_key(pool, key):
    await pool.execute_command("DEL", key)


async def set_redis_json(pool, key, obj, path="."):
    await pool.execute_command("JSON.SET", key, path, orjson.dumps(obj))


async def get_redis_json(pool, key, path="."):
    return orjson.loads(await pool.execute_command("JSON.GET", key, path))


async def del_redis_json(pool, key, path="."):
    await pool.execute_command("JSON.DEL", key, path)
