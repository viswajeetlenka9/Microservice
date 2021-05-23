import json
from flask import Flask

from services import root_dir, nice_json

app = Flask(__name__)

with open("{}/database/showtimes.json".format(root_dir()), "r") as f:
    showtimes = json.load(f)


@app.route("/", methods=["GET"])
def service_check():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "showtimes": "/showtimes",
            "showtime": "/showtimes/<date>"
        }
    })


@app.route("/showtimes", methods=["GET"])
def get_all_showtimes():
    return nice_json(showtimes)


@app.route("/showtimes/<date>", methods=["GET"])
def get_showtime_by_date(date):
    if date not in showtimes:
        return "No show found with date {}".format(date)

    return nice_json(showtimes[date])


if __name__ == "__main__":
    app.run(port=5003, debug=True)
