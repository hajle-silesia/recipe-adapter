import base64
import json
from pathlib import Path

from fastapi import FastAPI, Request

from src.file_content_monitor import FileContentMonitor
from src.notifier import Notifier
from src.storage import Storage

config_path = Path(__file__).parent / "../file_content_monitor/config.json"
recipe_path = Path(__file__).parent / "../recipe/recipe.xml"

app = FastAPI()

storage = Storage()
storage.path = config_path
notifier = Notifier(storage)
file_content_monitor = FileContentMonitor(notifier)
file_content_monitor.path = recipe_path


@app.get("/api")
async def api():
    return {"/content",
            "/observers",
            "/observers/register",
            "/observers/remove",
            }


@app.get("/content")
async def content():
    return {"content": file_content_monitor.content,
            }


@app.get("/observers")
async def observers():
    return notifier.observers


@app.post("/observers/register")
async def observers_register(request: Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    notifier.register_observer(request_body)


@app.post("/observers/remove")
async def observers_remove(request: Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    notifier.remove_observer(request_body)
