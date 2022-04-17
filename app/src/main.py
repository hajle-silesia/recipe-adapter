import uvicorn

from api import api

if __name__ == '__main__':
    uvicorn.run(api, port=5000)
