from flask import Flask
import json


app = Flask(__name__)


@app.route("/")
def hello_world():
    return json.dumps({"message": "hello Docker!"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
