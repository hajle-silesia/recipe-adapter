import base64
from pathlib import Path

from fastapi import FastAPI, Request

from src.file_content_monitor import FileContentMonitor
from src.notifier import Notifier
from src.storage import Storage

config_path = Path(__file__).parent / "../file_content_monitor/config.json"
recipe_path = Path(__file__).parent / "../recipe/recipe.xml"

api = FastAPI()

storage = Storage()
storage.path = config_path
notifier = Notifier(storage)
file_content_monitor = FileContentMonitor(notifier)
file_content_monitor.path = recipe_path


@api.get("/api")
async def content():
    return {"/content",
            "/observers",
            "/observers/register",
            "/observers/remove",
            }


@api.get("/content")
async def content():
    return {"content": file_content_monitor.content,
            }


@api.get("/observers")
async def observers():
    return notifier.observers


@api.post("/observers/register")
async def observers_register(request: Request):
    request_body = base64.b64decode(await request.body()).decode()
    notifier.register_observer(request_body)


@api.post("/observers/remove")
async def observers_remove(request: Request):
    request_body = base64.b64decode(await request.body()).decode()
    notifier.remove_observer(request_body)
