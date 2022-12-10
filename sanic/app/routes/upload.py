#!/usr/bin/env python3

"""This module defines the upload handler."""

import os

import aiofiles
import ujson as json
from sanic.log import logger
from sanic.response import redirect
from werkzeug.utils import secure_filename  # pylint: disable=C0411


async def write_file(path: str, body: bytes):  # pylint: disable=W0612
    """
    Asyncronycly writes a file to a given path.

    Attribures:
      path (str): Path to write file to.
      body (bytes): File body to write.
    """
    async with aiofiles.open(path, "wb") as f:
        await f.write(body)
    await f.close()


def valid_file_size(file_body: bytes, max_size: int = 10485760) -> bool:
    """
    Checks if the given file_body is below max_size.

    Attribures:
      file_body (bytes): File body to check.
      max_size (int): Maximum allowed size in bytes.
    """
    if len(file_body) < max_size:
        return True
    return False


def valid_file_type(file_name: str, file_type: str) -> bool:
    """
    Checks if the given file_name and file_type match certain criteria.

    Attribures:
      file_name (str): File name to check.
      file_type (str): File type to check.
    """
    file_name_type = file_name.split(".")[-1]
    if file_name_type == "pdf" and file_type == "application/pdf":
        # if file_type.split("/")[0] == "image":
        return True
    return True


async def upload(request):  # pylint: disable=W0612
    """
    Definition for upload handler.

    This handler allows to upload files to the server.

    Attributes:
      request (request): Reqest to handle.
    """
    if request.method == "POST":
        # Create upload folder if doesn't exist
        if not os.path.exists(request.app.config.UPLOAD_DIR):
            os.makedirs(request.app.config.UPLOAD_DIR)

        # Ensure a file was sent
        upload_file = request.files.get("file")
        if not upload_file:
            logger.error("No file")
            return redirect("/?error=no_file")

        # Clean up the filename in case it creates security risks
        filename = secure_filename(upload_file.name)

        # Ensure the file is a valid type and size, and if so
        # write the file to disk and redirect back to main
        if not valid_file_type(upload_file.name, upload_file.type):
            logger.error("Invalid file type")
            return redirect("/?error=invalid_file_type")
        if not valid_file_size(upload_file.body):
            logger.error("Invalid file size")
            return redirect("/?error=invalid_file_size")
        file_path = f"{request.app.config.UPLOADED_PATH}/{filename}"
        await write_file(file_path, upload_file.body)
        logger.info(
            json.dumps(
                {
                    "name": upload_file.name,
                    "type": upload_file.type,
                    "size": len(upload_file.body),
                }
            )
        )
        return redirect("/?error=none")
    return request.app.ctx.jinja.render(
        "dropzone.html", request, dropzone=request.app.ctx.dropzone
    )
