import base64
import json
import pathlib

import common.notifier
import common.storage
import fastapi

from src.file_content_monitor import FileContentMonitor

config_path = pathlib.Path(__file__).parent / "../file_content_monitor/config.json"
recipe_path = pathlib.Path(__file__).parent / "../recipe/recipe.xml"

app = fastapi.FastAPI()

storage = common.storage.Storage()
storage.path = config_path
notifier = common.notifier.Notifier(storage)
file_content_monitor = FileContentMonitor(notifier)
file_content_monitor.path = recipe_path


@app.get("/healthz")
async def healthz():
    return {'status': "ok"}


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
async def observers_register(request: fastapi.Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    notifier.register_observer(request_body)


@app.post("/observers/remove")
async def observers_remove(request: fastapi.Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    notifier.remove_observer(request_body)
