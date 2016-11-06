import os

from flask import Flask, jsonify, request, abort  # type: ignore
from werkzeug.exceptions import HTTPException  # type: ignore

from movie_api import MovieAPI

app = Flask(__name__)

GOOGLE_KEY = os.getenv('GOOGLE_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')
TMDB_KEY = os.getenv('TMDB_KEY')


@app.errorhandler(Exception)
@app.errorhandler(404)
@app.errorhandler(500)
def error_view(error):
    code = 500 if not isinstance(error, HTTPException) else error.code
    if request.is_json:
        return jsonify({
            'status_code': error.code,
            'response': str(error),
            'error': error.description
        }), code
    raise error.get_response()


@app.route('/api/search_movie', methods=['GET'])
def get_tasks():
    # assign GET parameters
    q = request.args.get('q')
    google_key = request.args.get('google_key', GOOGLE_KEY)
    google_cx = request.args.get('google_cx', GOOGLE_CX)
    tmdb_key = request.args.get('tmdb_key', TMDB_KEY)
    # configure API
    google = MovieAPI(google_key=google_key,
                      google_cx=google_cx,
                      tmdb_key=tmdb_key)
    # find movie based on its title
    imdb_id = google.find_movies(q)
    return jsonify({
        'data': imdb_id
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0')
