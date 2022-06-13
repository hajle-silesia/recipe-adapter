import base64
from pathlib import Path
import os
from fastapi import FastAPI

from src.file_content_monitor import FileContentMonitor

path = Path(__file__).parent / "../file_content_monitor/recipe.xml"
host = os.getenv('FILE_CONTENT_CONVERTER_SERVICE_HOST')
port = os.getenv('FILE_CONTENT_CONVERTER_SERVICE_PORT')
url = f"http://{host}:{port}/update"

api = FastAPI()
file_content_monitor = FileContentMonitor(path, url)


@api.get("/api")
async def content():
    return {"/content",
            }


@api.get("/content")
async def content():
    return {"content": file_content_monitor.content,
            }
