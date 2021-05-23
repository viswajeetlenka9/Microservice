import json
from flask import Flask

from services import root_dir, nice_json

app = Flask(__name__)

with open("{}/database/bookings.json".format(root_dir()), "r") as f:
    bookings = json.load(f)


@app.route("/", methods=["GET"])
def service_check():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "bookings": "/bookings",
            "booking": "/bookings/<username>"
        }
    })


@app.route("/bookings", methods=["GET"])
def get_all_bookings():
    return nice_json(bookings)


@app.route("/bookings/<username>", methods=["GET"])
def get_booking_by_username(username):
    if username not in bookings:
        return "No booking found with username {}".format(username)

    return nice_json(bookings[username])


if __name__ == "__main__":
    app.run(port=5001, debug=True)
