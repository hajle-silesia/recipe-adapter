import base64
import json
import pathlib

import fastapi
import kafka

from src.file_content_monitor import FileContentMonitor

recipe_path = pathlib.Path(__file__).parent / "../recipe/recipe.xml"

app = fastapi.FastAPI()

producer = kafka.KafkaProducer(bootstrap_servers="kafka-cluster-kafka-bootstrap.event-streaming:9092",
                               value_serializer=lambda message: base64.b64encode(
                                   json.dumps(message, default=str).encode()),
                               )
file_content_monitor = FileContentMonitor(producer)
file_content_monitor.path = recipe_path


@app.get("/healthz")
async def healthz():
    return {'status': "ok"}


@app.get("/content")
async def content():
    return {"content": file_content_monitor.content,
            }


@app.post("/update")
async def update(request: fastapi.Request):
    request_body_json = base64.b64decode(await request.body()).decode()
    request_body = json.loads(request_body_json)
    file_content_monitor.update(request_body)
    return {"status": "ok"}
