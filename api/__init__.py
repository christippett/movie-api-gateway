import logging
import os
import sys

from flask import Flask, jsonify, request, abort  # type: ignore
from werkzeug.exceptions import HTTPException  # type: ignore

from .movie_api import MovieAPI

GOOGLE_KEY = os.getenv('GOOGLE_KEY')
GOOGLE_CX = os.getenv('GOOGLE_CX')
TMDB_KEY = os.getenv('TMDB_KEY')

app = Flask(__name__)

# Configure logging
handler = logging.StreamHandler()
handler.setLevel(logging.NOTSET)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)


@app.errorhandler(Exception)
@app.errorhandler(404)
@app.errorhandler(500)
def error_view(error):
    code = 500 if not isinstance(error, HTTPException) else error.code
    return jsonify({
        'status_code': error.code,
        'response': str(error),
        'error': error.description
    }), code


@app.route('/api/search_movie', methods=['GET'])
def get_tasks():
    # get search term
    q = request.args.get('q')
    app.logger.info('Searching for "%s"' % q)

    # get API keys
    google_key = request.args.get('google_key', GOOGLE_KEY)
    google_cx = request.args.get('google_cx', GOOGLE_CX)
    tmdb_key = request.args.get('tmdb_key', TMDB_KEY)

    # configure API
    google = MovieAPI(google_key=google_key,
                      google_cx=google_cx,
                      tmdb_key=tmdb_key)

    # find movie based on its title
    movie_results = google.find_movies(q)
    if len(movie_results) == 0:
        app.logger.warning('No results found for search term "%s"' % q)
        response = 'No results found for search term "%s"' % q
    else:
        response = 'Success'

    app.logger.info('Finished fetching data for "%s"' % q)
    return jsonify({
        'data': movie_results,
        'response': response
    })
