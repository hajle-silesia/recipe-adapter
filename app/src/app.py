from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
async def hello_world():
    return {"message": "hello Docker!"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
