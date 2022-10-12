#!/usr/bin/env python3

import aiofiles
from sanic_ext import render
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic_dropzone import Dropzone


async def write_file(path, body):
    async with aiofiles.open(path, 'wb') as f:
        await f.write(body)
    f.close()

def valid_file_size(file_body, max_size=10485760):
    if len(file_body) < max_size:
        return True
    return False

def valid_file_type(file_name, file_type):
     file_name_type = file_name.split('.')[-1]
     if file_name_type == "pdf" and file_type == "application/pdf":
         return True
     return False

dropzone = Dropzone()

class ViewUpload(HTTPMethodView):
    decorators = []

    async def get(aelf, request):
        return await render('dropzone.html', request,
                context={"dropzone": request.app.ctx.extensions["dropzone"]})
    #context={"dropzone": dropzone})

    #@app.route('/upload2', methods=['POST', 'GET'])
    async def post(self, request):
        if request.method == 'POST':
            # Create upload folder if doesn't exist
            if not os.path.exists(app.config.UPLOAD_DIR):
                os.makedirs(app.config.UPLOAD_DIR)

            # Ensure a file was sent
            upload_file = request.files.get('file_names')
            if not upload_file:
                logger.error("No file")
                return redirect("/?error=no_file")

            # Clean up the filename in case it creates security risks
            filename = secure_filename(upload_file.name)

            # Ensure the file is a valid type and size, and if so
            # write the file to disk and redirect back to main
            if not valid_file_type(upload_file.name, upload_file.type):
                logger.error("Invalid file type")
                return redirect('/?error=invalid_file_type')
            elif not valid_file_size(upload_file.body):
                logger.error("Invalid file size")
                return redirect('/?error=invalid_file_size')
            else:
                file_path = f"{app.configUPLOADED_PATH}/{str(datetime.now())}.pdf"
                await write_file(file_path, upload_file.body)
                logger.info(json.dumps({"name": upload_file.name, "type": upload_file.type, "size": len(upload_file.body)}))
                return redirect('/?error=none')
