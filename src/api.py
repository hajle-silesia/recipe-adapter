import base64
from pathlib import Path

from fastapi import FastAPI

from src.file_content_monitor import FileContentMonitor

api = FastAPI()
file_content_monitor = FileContentMonitor(Path(__file__).parent / "../file_content_monitor/recipe.xml")


@api.get("/content")
async def content():
    return {"content": base64.b64encode(file_content_monitor.content.encode()),
            }
