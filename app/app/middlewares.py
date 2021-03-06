# middlewares.py
import aiohttp_jinja2
from aiohttp import web
from aiohttp_security import authorized_userid, check_authorized
from aiohttp_session import get_session

http_errors = {
    401: {
        "status": 401,
        "status_message": "Unauthorized",
        "message": "The request requires user authentication.",
        "append": [{"loginform": "loginform"}],
    },
    403: {
        "status": 403,
        "status_message": "Forbidden",
        "message": """The server understood the request, but is refusing to
            fulfill it. Authorization will not help and the request SHOULD
            NOT be repeated.""",
        "append": [],
    },
    404: {
        "status": 404,
        "status_message": "Not Found",
        "message": """The server has not found anything matching the
            Request-URI. No indication is given of whether the condition is
            temporary or permanent.""",
        "append": [],
    },
    405: {
        "status": 405,
        "status_message": "Method not allowed",
        "message": """The method specified in the Request-Line is not allowed
            for the resource identified by the Request-URI. The response MUST
            include an Allow header containing a list of valid methods for the
            requested resource.""",
        "append": [],
    },
    500: {
        "status": 500,
        "status_message": "Internal Server Error",
        "message": """The server encountered an unexpected condition which
            prevented it from fulfilling the request.""",
        "append": ["exception"],
    },
}


async def handle_401(request):
    # Unauthorized
    return aiohttp_jinja2.render_template(
        "error.html", request, http_errors[401], status=401
    )


async def handle_403(request):
    # Forbidden
    return aiohttp_jinja2.render_template(
        "error.html", request, http_errors[403], status=403
    )


async def handle_404(request):
    # NotFound
    return aiohttp_jinja2.render_template(
        "error.html", request, http_errors[404], status=404
    )


async def handle_405(request):
    # MethodNotAllowed
    return aiohttp_jinja2.render_template(
        "error.html", request, http_errors[405], status=405
    )


async def handle_500(request):
    # InternalServerError
    context = http_errors[500]
    context["append"] = {"exception": str(request["error"])}
    return aiohttp_jinja2.render_template(
        "error.html", request, http_errors[500], status=500
    )


def create_error_middleware(overrides):
    @web.middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise
        except Exception as e:
            request["error"] = e
            return await handler(request)
            # return await overrides[500](request)

    return error_middleware


@web.middleware
async def session_middleware(request, handler):
    request["session"] = await get_session(request)
    return await handler(request)


@web.middleware
async def login_middleware(request, handler):
    request["user"] = None
    username = await authorized_userid(request)
    if username:
        await check_authorized(request)
        request["user"] = username
    return await handler(request)


async def setup_middlewares(app):
    error_middleware = create_error_middleware(
        {
            401: handle_401,
            403: handle_403,
            404: handle_404,
            405: handle_405,
            #            500: handle_500,
        }
    )
    app.middlewares.append(error_middleware)
    app.middlewares.append(session_middleware)
    app.middlewares.append(login_middleware)
