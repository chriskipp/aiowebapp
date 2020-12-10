import asyncio
from collections import defaultdict

import pytest
from aiohttp import web
from aiohttp_session import get_session

from app.auth import AuthorizationPolicy, check_credentials
from app.main import create_app
from app.session import setup_security, setup_session


logins = [
    {
        "user": "user",
        "password": "password",
        "check_credentials": True,
        "authorized_userid": "user",
    },
    {
        "user": "user",
        "password": "wrong_password",
        "check_credentials": False,
        "authorized_userid": "user",
    },
    {
        "user": "moderator",
        "password": "wrong_password",
        "check_credentials": False,
        "authorized_userid": "moderator",
    },
    {
        "user": "moderator",
        "password": "password",
        "check_credentials": True,
        "authorized_userid": "moderator",
    },
    {
        "user": "admin",
        "password": "password",
        "check_credentials": True,
        "authorized_userid": "admin",
    },
    {
        "user": "admin",
        "password": "wrong_password",
        "check_credentials": False,
        "authorized_userid": "admin",
    },
    {
        "user": "nologin",
        "password": "password",
        "check_credentials": False,
        "authorized_userid": None,
    },
]

user_permissions = {
    "admin": {"public", "protected"},
    "moderator": {"public", "protected"},
    "user": {"public"},
}
# user_permissions = itertools.chain(*[[(u,p) for p in user_permissions[u]] for u, p in user_permissions.items()])


def combine(seq1, seq2):
    for i1 in seq1:
        for i2 in seq2:
            yield i1, i2


users = ["admin", "moderator", "user", "nologin", None]
permissions = ["public", "protected"]

user_permissions = combine(users, permissions)

user_permission = defaultdict(
    set,
    {
        "admin": {"public", "protected"},
        "moderator": {"public", "protected"},
        "user": {"public"},
    },
)


@pytest.mark.parametrize("login", logins)
async def test_login_check_credentials(login):
    app = create_app()
    await setup_security(app)

    res = await check_credentials(app["dbsa"], login["user"], login["password"])
    assert res == login["check_credentials"]


@pytest.mark.parametrize("login", logins)
async def test_login_authorized_userid(login):

    app = create_app()
    await setup_security(app)
    policy = AuthorizationPolicy(app["dbsa"])

    res = await policy.authorized_userid(login["user"])
    assert res == login["authorized_userid"]


@pytest.mark.parametrize("user,permission", user_permissions)
async def test_login_permit(user, permission):
    app = create_app()
    await setup_security(app)
    policy = AuthorizationPolicy(app["dbsa"])

    if permission in user_permission[user]:
        assert await policy.permits(user, permission)
    else:
        assert not await policy.permits(user, permission)


async def test_loginhandler_login(aiohttp_client):
    users = ["user", "moderator", "admin"]
    nousers = ["nouser", None]

    async def identity(request):
        session = await get_session(request)
        if "logSessionId" in session.keys():
            return web.Response(text=session["logSessionId"])
        else:
            return web.Response(text="")

    app = create_app()
    await setup_session(app)
    await setup_security(app)
    app.router.add_get("/identity", identity)
    client = await aiohttp_client(app)

    for user in users:
        res = await client.post("/login", data={"login": user, "password": "password"})
        assert res.status == 200
        res = await client.get("/identity")
        assert res.status == 200
        txt = await res.text()
        assert txt == user

        res = await client.get("/logout")
        res = await client.get("/identity")
        assert res.status == 200
        txt = await res.text()
        assert txt == ""

    for nouser in nousers:
        res = await client.post(
            "/login", data={"login": nouser, "password": "password"}
        )
        assert res.status == 401
        res = await client.get("/identity")
        assert res.status == 200
        txt = await res.text()
        assert txt == ""

        res = await client.get("/logout")
        assert res.status == 401
        res = await client.get("/identity")
        assert res.status == 200
        txt = await res.text()
        assert txt == ""
