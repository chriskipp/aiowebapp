from pathlib import Path

import orjson
import pytest

from app.main import create_app
from app.redis import (del_redis_json, del_redis_key, get_redis_json,
                       get_redis_key, set_redis_json, set_redis_key,
                       setup_redis, teardown_redis)

redis_keys = [
    ("test", "test"),
    ("test", ""),
    ("test", 1),
    ("test", 0.1),
    ("test", True),
    ("test", False),
    ("test", None),
]


def get_json_objs():
    path = Path("tests/data")
    for jsonf in path.glob("*.json"):
        with open(jsonf) as f:
            json_obj = orjson.loads(f.read())
            yield ("test", json_obj)


json_objs = get_json_objs()


@pytest.fixture()
async def create_app_with_redis():
    app = create_app()
    await setup_redis(app)
    yield app
    await teardown_redis(app)


#@pytest.mark.asyncio
#async def test_redis_setup_teardown(create_app_with_redis):
#    app = create_app_with_redis
#
#    assert "redis" in app.keys()
#    await teardown_redis(app)
#    assert app["redis"].closed


@pytest.mark.asyncio
@pytest.mark.parametrize(("key", "value"), redis_keys)
async def test_set_get_del_keys(create_app_with_redis, key, value):
    app = create_app_with_redis

    await set_redis_key(app["redis"], key, value)
    res = await get_redis_key(app["redis"], key)
    assert res == value

    await del_redis_key(app["redis"], key)
    res = await get_redis_key(app["redis"], key)
    assert res is None


@pytest.mark.asyncio
@pytest.mark.parametrize(("key", "value"), json_objs)
async def test_get_set_del_json(create_app_with_redis, key, value):
    app = create_app_with_redis

    await set_redis_json(app["redis"], key, value)
    res = await get_redis_json(app["redis"], key)
    assert res == res

    res = await del_redis_json(app["redis"], key)
    assert res is None


@pytest.mark.asyncio
@pytest.mark.parametrize("module", ["ReJSON", "search"])
async def test_redis_modules(create_app_with_redis, module):
    app = create_app_with_redis

    modules = await app["redis"].execute_command("MODULE LIST")
    modules = {m[1].decode() for m in modules}
    assert module in modules
