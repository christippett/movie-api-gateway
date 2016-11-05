from functools import wraps

from flask import Flask, abort, jsonify, make_response, request  # type: ignore
from werkzeug.exceptions import HTTPException  # type: ignore

from movie_api import MovieAPI

app = Flask(__name__)


@app.errorhandler(Exception)
def not_found(error):  # pylint: disable=W0613
    code = 500 if not isinstance(error, HTTPException) else error.code
    if request.is_json:
        return jsonify({
            'status_code': error.code,
            'message': str(error),
            'description': error.description
        }), error.code
    raise error.get_response()


@app.route('/api/search_movie', methods=['GET'])
def get_tasks():
    q = request.args.get('q')
    google = MovieAPI(google_key='AIzaSyDnB2uWxHZ9CKVCR6lzXJGynvVcxJFyIaM',
                      google_cx='015622078606278990278:5t6sqmzziik',
                      tmdb_key='2833b819ebafbb620ae46298a22abae8')
    imdb_id = google.find_movies(q)
    return jsonify({
        'data': imdb_id
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0')
