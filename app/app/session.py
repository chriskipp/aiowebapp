# session.py

import aioredis
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import setup as securitysetup
from aiohttp_session import setup as sessionsetup
from aiohttp_session.redis_storage import RedisStorage

from app.auth import AuthorizationPolicy
from app.db import setup_pgsa


async def setup_session(app):
    conf = app["config"]["redis"]
    redis_address = "redis://" + conf["host"] + ":" + str(conf["port"])
    redis_pool = await aioredis.create_redis_pool(redis_address)
    app["session_pool"] = redis_pool
    storage = RedisStorage(redis_pool)

    sessionsetup(app, storage)


async def teardown_session(app):
    app["session_pool"].close()
    await app["session_pool"].wait_closed()


async def setup_security(app):
    await setup_pgsa(app)
    securitysetup(app, SessionIdentityPolicy(), AuthorizationPolicy(app["dbsa"]))
