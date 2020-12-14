# middlewares.py
import aiohttp_jinja2
from aiohttp import web


async def handle_401(request):
    # Unauthorized
    return aiohttp_jinja2.render_template(
        "error.html", request, {"status": 401}, status=401
    )


async def handle_403(request):
    # Forbidden
    return aiohttp_jinja2.render_template(
        "error.html", request, {"status": 403}, status=403
    )


async def handle_404(request):
    # NotFound
    return aiohttp_jinja2.render_template(
        "error.html", request, {"status": 404}, status=404
    )


async def handle_405(request):
    # MethodNotAllowed
    return aiohttp_jinja2.render_template(
        "error.html", request, {"status": 405}, status=405
    )


async def handle_500(request):
    # InternalServerError
    return aiohttp_jinja2.render_template(
        "error.html", request, {"status": 500}, status=500
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
        except Exception:
            return await overrides[500](request)

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware(
        {
            401: handle_401,
            403: handle_403,
            404: handle_404,
            405: handle_405,
            500: handle_500,
        }
    )
    app.middlewares.append(error_middleware)
