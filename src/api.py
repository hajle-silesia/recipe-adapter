import base64
from pathlib import Path

from fastapi import FastAPI

from src.file_content_monitor import FileContentMonitor

api = FastAPI()


@api.get("/api")
async def content():
    return {"/content",
            }


@api.get("/content")
async def content():
    return {"content": base64.b64encode(file_content_monitor.content.encode()),
            }
