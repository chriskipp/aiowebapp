
import pathlib
import aiohttp
from aiohttp import web
import aiohttp_jinja2

from .base import BaseHandler

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
PROJECT_ROOT = BASE_DIR / "app"

class DataHandler(BaseHandler):
    async def fileUploadFormHandler(self, request):
        context=await self.get_context(request, {})
        context["target_uploadFiles"] = "/upload"
        response = aiohttp_jinja2.render_template(
            "uploadFiles.html",
            request,
            context=context
        )
        return response
    
    
    async def fileUploadHandler(self, request):
        reader = await request.multipart()
        response = ""
        while True:
            part = await reader.next()
            if part is None:
                break
            if part.name == "fileUpload":
                headers = part.headers
                contentType = part.headers[aiohttp.hdrs.CONTENT_TYPE]
                filename = part.filename
                size = 0
                uploadPath = PROJECT_ROOT / "storage/uploads" / filename
                if not uploadPath.parent.is_dir():
                    try:
                        uploadPath.parent.mkdir(mode=755, parents=True, exist_ok=True)
                    except:
                        continue
                with open(uploadPath, "wb") as f:
                    while True:
                        chunk = await part.read_chunk()
                        if not chunk:
                            break
                        size += len(chunk)
                        f.write(chunk)
                response += "\n{} sized of {} successfully stored".format(filename, size)
        return web.Response(text=response)
    

    def configure(self, app):

        router = app.router
        router.add_route("GET", "/upload", self.fileUploadFormHandler, name="fileUpload")
        router.add_route("POST", "/upload", self.fileUploadHandler, name="upload")
