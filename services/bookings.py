import json
from flask import Flask

from services import root_dir, nice_json

app = Flask(__name__)

with open("{}/database/bookings.json".format(root_dir()), "r") as f:
    bookings = json.load(f)


@app.route("/", methods=["GET"])
def service_check():
    return "Booking service running!"


if __name__ == "__main__":
    app.run(port=5001, debug=True)
