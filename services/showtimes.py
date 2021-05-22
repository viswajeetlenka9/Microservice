import json
from flask import Flask

from services import root_dir, nice_json

app = Flask(__name__)

with open("{}/database/showtimes.json".format(root_dir()), "r") as f:
    showtimes = json.load(f)


@app.route("/", methods=["GET"])
def service_check():
    return "Show times service running!"


if __name__ == "__main__":
    app.run(port=5003, debug=True)
