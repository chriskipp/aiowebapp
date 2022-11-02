#!/usr/bin/env python3

#from sanic_ext import render

async def index(request):
    request.app.ctx.jinja.session(request)["user"] = "session user"
    request.app.ctx.jinja.flash(request, "success message", "success")
    request.app.ctx.jinja.flash(request, "info message", "info")
    request.app.ctx.jinja.flash(request, "warning message", "warning")
    request.app.ctx.jinja.flash(request, "error message", "error")
    return request.app.ctx.jinja.render("index.html", request, greetings="blub")

