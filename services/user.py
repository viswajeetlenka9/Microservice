import json
import requests
from flask import Flask

from services import root_dir, nice_json

app = Flask(__name__)

with open("{}/database/users.json".format(root_dir()), "r") as f:
    users = json.load(f)


@app.route("/", methods=["GET"])
def service_check():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "users": "/users",
            "user": "/users/<username>",
            "bookings": "/users/<username>/bookings"
        }
    })


@app.route("/users", methods=["GET"])
def get_all_users():
    return nice_json(users)


@app.route("/users/<username>", methods=["GET"])
def get_user_by_username(username):
    if username not in users:
        return "No user found with username {}".format(username)

    return nice_json(users[username])


@app.route("/users/<username>/bookings", methods=["GET"])
def get_user_bookings_by_username(username):
    if username not in users:
        return "No user found with username {}".format(username)

    try:
        user_bookings = requests.get("http://127.0.0.1:5001/bookings/{}".format(username))
    except requests.exceptions.ConnectionError:
        return "The Bookings service is unavailable."

    if user_bookings.status_code == 404:
        return "No bookings were found for {}".format(username)

    user_bookings = user_bookings.json()

    result = {}
    for date, movies in user_bookings.items():

        result[date] = []
        for movie_id in movies:
            try:
                movie_response = requests.get("http://127.0.0.1:5002/movies/{}".format(movie_id))
            except requests.exceptions.ConnectionError:
                return "The Movie service is unavailable."

            movie_response = movie_response.json()
            result[date].append({
                "title": movie_response["title"],
                "rating": movie_response["rating"],
                "url": movie_response["url"]
            })
    return nice_json(result)


if __name__ == "__main__":
    app.run(port=5004, debug=True)
