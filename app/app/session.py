# session.py

import aioredis
from aiohttp_security import SessionIdentityPolicy
from aiohttp_security import setup as securitysetup
from aiohttp_session import setup as sessionsetup
#from aiohttp_session.redis_storage import RedisStorage
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from app.auth import AuthorizationPolicy
from app.db import setup_pgsa


async def setup_session(app):
    conf = app["config"]["redis"]
    redis_address = "redis://" + conf["host"] + ":" + str(conf["port"])
    redis_pool = aioredis.from_url(
            redis_address, encoding="utf-8", decode_responses=True
    )
    app["session_pool"] = redis_pool
    #storage = RedisStorage(redis_pool)
    storage = EncryptedCookieStorage(b'Thirty  two  length  bytes  key.')

    sessionsetup(app, storage)


async def teardown_session(app):
    app["session_pool"].close()


async def setup_security(app):
    await setup_pgsa(app)
    securitysetup(
        app,
        SessionIdentityPolicy(session_key="logSessionId"),
        AuthorizationPolicy(app["dbsa"]),
    )
