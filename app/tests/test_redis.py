import asyncio

from app.main import create_app
from app.redis import (
    del_redis_key,
    get_redis_json,
    get_redis_key,
    set_redis_json,
    set_redis_key,
    setup_redis,
    teardown_redis,
)

loop = asyncio.get_event_loop()


async def test_redis_setup_teardown(loop=loop):
    app = create_app(loop)
    await setup_redis(app)
    assert "redis" in {k for k in app.keys()}
    await teardown_redis(app)
    assert app["redis"].closed


async def test_redis_keys(loop=loop):
    app = create_app(loop)
    await setup_redis(app)

    await set_redis_key(app["redis"], "test_key", "test_value")
    v = await get_redis_key(app["redis"], "test_key")
    assert v == "test_value"
    await del_redis_key(app["redis"], "test_key")
    v = await get_redis_key(app["redis"], "test_key")
    assert v == None


async def test_redis_set_json(loop=loop):
    json_obj = {"a": 1, "b": 2, "c": 3}
    app = create_app(loop)
    await setup_redis(app)

    await set_redis_json(app["redis"], "test_obj", json_obj)
    res = await get_redis_json(app["redis"], "test_obj")
    assert res == json_obj


async def test_redis_modules(loop=loop):
    app = create_app(loop)
    await setup_redis(app)

    pool = app["redis"]
    modules = await pool.execute("MODULE", "LIST")
    modules = {m[1].decode() for m in modules}
    assert "ReJSON" in modules
    assert "search" in modules
