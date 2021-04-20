import aiohttp_jinja2
import pytest

from app.main import create_app

users = ["admin", "user", "moderator", None]

routes_get = {
    "/": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/login": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/session": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/me": {"admin": 200, "user": 200, "moderator": 200, None: 401},
    "/users/1": {"admin": 200, "user": 200, "moderator": 200, None: 401},
    "/public": {"admin": 200, "user": 200, "moderator": 200, None: 401},
    "/protected": {"admin": 200, "user": 403, "moderator": 200, None: 401},
    "/storage": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/search": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/redis": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/logout": {"admin": 200, "user": 200, "moderator": 200, None: 401},
    "/editor": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/map": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/nominatim": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/database": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/upload": {"admin": 200, "user": 200, "moderator": 200, None: 200},
    "/static/images/favicon.ico": {
        "admin": 200,
        "user": 200,
        "moderator": 200,
        None: 200,
    },
    "/not_defined_route": {
        "admin": 404,
        "user": 404,
        "moderator": 404,
        None: 404,
    },
}

routes_post = {
    "/autocomplete": {
        "admin": 200,
        "user": 200,
        "moderator": 200,
        None: 200,
        "data": {"q": "cat"},
        "response": '{"results": [{"id": "cat", "text": "cat"}, {"id": "catman", "text": "catman"}, {"id": "catchsegv", "text": "catchsegv"}]}',
    },
    "/search": {
        "admin": 200,
        "user": 200,
        "moderator": 200,
        None: 200,
        "data": {"q": "cat"},
        "response": '{"total": 61, "results": [{"body":',
        "response_chars": 34,
    },
    "/database": {
        "admin": 200,
        "user": 200,
        "moderator": 200,
        None: 200,
        "data": '{"query": "SELECT 1 FROM information_schema.columns LIMIT 1;"}',
        "response": '[{"?column?":1}]',
    },
}

routes_post_file = {
    "/upload": {
        "admin": 200,
        "user": 200,
        "moderator": 200,
        None: 200,
    }
}


async def test_internal_server_error(aiohttp_client):
    async def internal_server_error(request):
        return aiohttp_jinja2.render_template(
            "layout.html", request, context=""
        )

    app = create_app()
    app.router.add_get("/error", internal_server_error)
    client = await aiohttp_client(app)

    res = await client.get("/error")
    assert res.status == 500


async def test_handler_exception(aiohttp_client):
    async def exception(request):
        raise Exception

    app = create_app()
    app.router.add_get("/exception", exception)
    client = await aiohttp_client(app)

    res = await client.get("/exception")
    assert res.status == 500


@pytest.mark.parametrize(("route"), routes_get.keys())
@pytest.mark.parametrize(("user"), users)
async def test_route_get(aiohttp_client, route, user):

    app = create_app()
    client = await aiohttp_client(app)

    if user:
        res = await client.get("/session")
        res = await client.post(
            "/login", data={"loginField": user, "passwordField": "password"}
        )
        assert res.status == 200

    res = await client.get(route)
    assert res.status == routes_get[route][user]


@pytest.mark.parametrize(("route"), routes_post.keys())
@pytest.mark.parametrize(("user"), users)
async def test_route_post(aiohttp_client, route, user):

    app = create_app()
    client = await aiohttp_client(app)

    if user:
        res = await client.get("/session")
        res = await client.post(
            "/login", data={"loginField": user, "passwordField": "password"}
        )
        assert res.status == 200

    res = await client.post(route, data=routes_post[route]["data"])
    assert res.status == routes_post[route][user]
    if "response" in routes_post[route].keys():
        text = await res.text()
        if "response_chars" in routes_post[route].keys():
            assert (
                text[: routes_post[route]["response_chars"]]
                == routes_post[route]["response"]
            )
        else:
            assert text == routes_post[route]["response"]


@pytest.mark.parametrize(("route"), routes_post_file.keys())
@pytest.mark.parametrize(("user"), users)
async def test_route_post_file(aiohttp_client, route, user):

    app = create_app()
    client = await aiohttp_client(app)

    if user:
        res = await client.get("/session")
        res = await client.post(
            "/login", data={"loginField": user, "passwordField": "password"}
        )
        assert res.status == 200

    with open("run.sh", "rb") as f:
        res = await client.post(route, data={"fileUpload": f})
    assert res.status == routes_post_file[route][user]


async def test_method_not_allowed(aiohttp_client):

    client = await aiohttp_client(create_app())

    res = await client.post("/logout", data={"some": "data"})
    assert res.status == 405
