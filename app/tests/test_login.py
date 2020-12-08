import asyncio

from aiohttp import web
from aiohttp_session import get_session

from app.auth import AuthorizationPolicy, check_credentials
from app.main import create_app
from app.session import setup_security, setup_session

loop = asyncio.get_event_loop()


async def test_login_check_credentials(loop=loop):
    users = ["user", "moderator", "admin"]
    password = "password"

    app = create_app(loop)
    await setup_security(app)

    for user in users:
        assert await check_credentials(app["dbsa"], user, password)
    assert not await check_credentials(app["dbsa"], "nouser", password)


async def test_login_authorized_userid(loop=loop):
    users = ["user", "moderator", "admin"]
    nousers = ["nouser", None]

    app = create_app(loop)
    await setup_security(app)
    policy = AuthorizationPolicy(app["dbsa"])

    for user in users:
        authorized_id = await policy.authorized_userid(user)
        assert authorized_id == user
    for nouser in nousers:
        authorized_id = await policy.authorized_userid(nouser)
        assert authorized_id == None


async def test_login_permit(loop=loop):
    users = {
        "admin": {"public", "protected"},
        "moderator": {"public", "protected"},
        "user": {"public"},
    }
    nousers = ["nouser", None]
    permissions = ["public", "protected"]

    app = create_app(loop)
    await setup_security(app)
    policy = AuthorizationPolicy(app["dbsa"])

    for user in users:
        for permission in permissions:
            if permission in users[user]:
                assert await policy.permits(user, permission)
            else:
                assert not await policy.permits(user, permission)

    for nouser in nousers:
        for permission in permissions:
            has_accsess = await policy.permits(nouser, permission)
            assert has_accsess == False


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
