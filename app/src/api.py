import base64

from fastapi import FastAPI

from file_content_monitor import FileContentMonitor


api = FastAPI()
file_content_monitor = FileContentMonitor("./file_content_monitor/recipe.xml")


@api.get("/content")
async def content():
    return {"content": base64.b64encode(file_content_monitor.content.encode()),
            }
