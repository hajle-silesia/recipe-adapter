from fastapi import FastAPI
from file_content_monitor import FileContentMonitor


api = FastAPI()
file_content_monitor = FileContentMonitor("./test.txt")


@api.get("/content")
async def content():
    return {"content": file_content_monitor.content,
            }
