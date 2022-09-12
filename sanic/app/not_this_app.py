#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic_session import InMemorySessionInterface
from sanic_jinja2 import SanicJinja2
from sanic.response import redirect

app = Sanic(__name__)

jinja = SanicJinja2(app, pkg_name='static')

session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    await session.open(request)


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    await session.save(request, response)

@app.route("/")
async def index(request):
    return redirect("index.html")


#@app.websocket("/feed")
#async def feed(request, ws):
#    while True:
#        data = "hello!"
#        print("Sending: " + data)
#        await ws.send(data)
#        data = await ws.recv()
#        print("Received: " + data)


@app.route('/index.html')
async def index(request):
    return jinja.render(
        'index.html',
        request, greetings='Hello, sanic!'
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
