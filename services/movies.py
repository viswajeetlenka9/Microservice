import json
from flask import Flask

from services import root_dir, nice_json

app = Flask(__name__)

with open("{}/database/movies.json".format(root_dir()), "r") as f:
    movies = json.load(f)


@app.route("/", methods=["GET"])
def service_check():
    return "Movies service running!"


if __name__ == "__main__":
    app.run(port=5002, debug=True)
