#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import aiofiles
import ujson as json
from sanic.log import logger
from sanic_dropzone import Dropzone
from sanic_jinja2 import SanicJinja2
from sanic_session import InMemorySessionInterface, Session
from werkzeug.utils import secure_filename

from sanic import Sanic

basedir = os.path.abspath(os.path.dirname(__file__))

#app = Sanic(__name__.replace('.', '_'))

#session = Session(app, interface=InMemorySessionInterface())
#jinja = SanicJinja2(app, session=session)

#dropzone = Dropzone(app)

config = {
    "HOST": '0.0.0.0',
    "PORT": 8000,
    "DEBUG": True,
    "WORKERS": 4,

    "SECRET_KEY": 'dev key',  # the secret key used to generate CSRF token

    "UPLOADED_PATH": os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    "DROPZONE_ALLOWED_FILE_TYPE": 'image',
    "DROPZONE_MAX_FILE_SIZE": 3, # MB
    "DROPZONE_MAX_FILES": 30,
    "DROPZONE_UPLOAD_MULTIPLE":  True,  # enable parallel upload
    "DROPZONE_PARALLEL_UPLOADS":  10,  # handle 3 file per request
    "DROPZONE_ENABLE_CSRF":  True,  # enable CSRF protection


    "FORWARDED_SECRET": "YOUR SECRET"
}

# Serves files from the static folder to the URL /static
#app.static('/static', './static')

#@app.route("/", methods=["GET", "POST"])
#async def index(request):
#    jinja.session(request)["user"] = "session user"
#    jinja.flash(request, "success message", "success")
#    jinja.flash(request, "info message", "info")
#    jinja.flash(request, "warning message", "warning")
#    jinja.flash(request, "error message", "error")
#    #return jinja.render('index.html', request, greetings="Hello, sanic!")
#    return jinja.render('layout.html', request, greetings="Hello, sanic!")
#
#@app.route('/upload', methods=['POST', 'GET'])
#async def upload(request):
#    if request.method == 'POST':
#        f = request.files.get('file')
#        logger.info(json.dumps({"name": f.name, "type": f.type, "size": len(f.body)}))
#        file_path = os.path.join(app.config['UPLOADED_PATH'], f.name)
#
#        if not os.path.exists(app.config['UPLOADED_PATH']):
#            os.makedirs(app.config["UPLOADED_PATH"])
#
#        upload_path = app.config["UPLOADED_PATH"] + "/" + request.files["file"][0].name
#        async with aiofiles.open(upload_path, 'wb') as f:
#            await f.write(request.files["file"][0].body)
#            f.close()
#        # You can return a JSON response then get it on client side:
#        # (see template index.html for client implementation)
#        # return jsonify(uploaded_path=file_path)
#    return jinja.render('dropzone.html', request, dropzone=dropzone)

def create_app():
    app = Sanic(__name__.replace('.', '_'))

    app.config.update(config)

    from .upload import ViewUpload
    app.add_route(ViewUpload.as_view(), '/upload2')

    session = Session(app, interface=InMemorySessionInterface())
    jinja = SanicJinja2(app, session=session)

    dropzone = Dropzone(app)
    #dropzone = Dropzone()
    #dropzone.init(app)

    # Serves files from the static folder to the URL /static
    app.static('/static', './static')

    return app



if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
