from collections import defaultdict

import pytest

from app.auth import AuthorizationPolicy, check_credentials
from app.main import create_app
from app.session import setup_security

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

    res = await check_credentials(
        app["dbsa"], login["user"], login["password"]
    )
    assert res == login["check_credentials"]


@pytest.mark.parametrize("login", logins)
async def test_login_authorized_userid(login):

    app = create_app()
    await setup_security(app)
    policy = AuthorizationPolicy(app["dbsa"])

    res = await policy.authorized_userid(login["user"])
    assert res == login["authorized_userid"]


@pytest.mark.parametrize(("user", "permission"), user_permissions)
async def test_login_permit(user, permission):
    app = create_app()
    await setup_security(app)
    policy = AuthorizationPolicy(app["dbsa"])

    if permission in user_permission[user]:
        assert await policy.permits(user, permission)
    else:
        assert not await policy.permits(user, permission)


@pytest.mark.parametrize("user", users)
async def test_loginhandler_login(aiohttp_client, user):

    app = create_app()
    client = await aiohttp_client(app)

    if True:
        res = await client.post(
            "/login", data={"loginField": user, "passwordField": "password"}
        )
        if res.status == 200:
            res = await client.get("/identity")
            assert res.status == 200
            txt = await res.text()
            assert txt == user

        if res.status == 401:
            res = await client.get("/identity")
            assert res.status == 200
            txt = await res.text()
            assert txt == ""

        res = await client.get("/logout")
        res = await client.get("/identity")
        assert res.status == 200
        txt = await res.text()
        assert txt == ""
