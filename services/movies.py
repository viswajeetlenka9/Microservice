import json
from flask import Flask

from services import root_dir, nice_json

app = Flask(__name__)

with open("{}/database/movies.json".format(root_dir()), "r") as f:
    movies = json.load(f)


@app.route("/", methods=["GET"])
def service_check():
    return nice_json({
        "uri": "/",
        "subresource_uris": {
            "movies": "/movies",
            "movie": "/movies/<id>"
        }
    })


@app.route("/movies", methods=["GET"])
def get_all_movies():
    return nice_json(movies)


@app.route("/movies/<movie_id>", methods=["GET"])
def get_movie_by_movie_id(movie_id):
    if movie_id not in movies:
        return "No movie found with movie_id {}".format(movie_id)

    result = movies[movie_id]
    result["url"] = "/movies/{}".format(movie_id)

    return nice_json(result)


if __name__ == "__main__":
    app.run(port=5002, debug=True)
