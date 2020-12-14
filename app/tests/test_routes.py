import pytest

from app.main import create_app
from app.session import setup_security, setup_session

routes_nologin = [
    ("/", 200),
    ("/login", 200),
    ("/session", 200),
    ("/users/me", 401),
    ("/users/1", 401),
    ("/public", 401),
    ("/protected", 401),
    ("/storage", 200),
    ("/logout", 401),
    ("/static/images/favicon.ico", 200),
    ("/not_defined_route", 404),
]

routes_user = [
    ("/", 200),
    ("/login", 200),
    ("/session", 200),
    ("/users/me", 200),
    ("/users/1", 200),
    ("/public", 200),
    ("/protected", 403),
    ("/storage", 200),
    ("/logout", 200),
    ("/not_defined_route", 404),
]

routes_moderator = [
    ("/", 200),
    ("/login", 200),
    ("/session", 200),
    ("/users/me", 200),
    ("/users/1", 200),
    ("/public", 200),
    ("/protected", 200),
    ("/storage", 200),
    ("/logout", 200),
    ("/not_defined_route", 404),
]

routes_admin = [
    ("/", 200),
    ("/login", 200),
    ("/session", 200),
    ("/users/me", 200),
    ("/users/1", 200),
    ("/public", 200),
    ("/protected", 200),
    ("/storage", 200),
    ("/logout", 200),
]


@pytest.mark.parametrize("route,status", routes_nologin)
async def test_route_nologin(aiohttp_client, route, status):
    client = await aiohttp_client(create_app())
    res = await client.get(route)
    assert res.status == status


@pytest.mark.parametrize("route,status", routes_admin)
async def test_route_admin(aiohttp_client, route, status):

    app = create_app()
    await setup_session(app)
    await setup_security(app)
    client = await aiohttp_client(app)

    res = await client.post(
        "/login", data={"loginField": "admin", "passwordField": "password"}
    )
    assert res.status == 200

    res = await client.get(route)
    assert res.status == status


@pytest.mark.parametrize("route,status", routes_user)
async def test_route_user(aiohttp_client, route, status):

    app = create_app()
    await setup_session(app)
    await setup_security(app)
    client = await aiohttp_client(app)

    res = await client.post(
        "/login", data={"loginField": "user", "passwordField": "password"}
    )
    assert res.status == 200

    res = await client.get(route)
    assert res.status == status


@pytest.mark.parametrize("route,status", routes_moderator)
async def test_route_moderator(aiohttp_client, route, status):

    app = create_app()
    await setup_session(app)
    await setup_security(app)
    client = await aiohttp_client(app)

    res = await client.post(
        "/login", data={"loginField": "moderator", "passwordField": "password"}
    )
    assert res.status == 200

    res = await client.get(route)
    assert res.status == status
