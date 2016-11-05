import logging
import re
from typing import List, Dict

import requests

from .tmdb import TMDbAPI


class GoogleAPIError(ConnectionError):
    pass


class OMDBAPIError(ConnectionError):
    pass


class MovieAPI(object):
    GoogleAPIError = GoogleAPIError
    OMDBAPIError = OMDBAPIError
    google_url = 'https://www.googleapis.com/customsearch/v1'
    omdb_url = 'http://www.omdbapi.com/'
    tmdb_url = 'http://api.themoviedb.org/3/'

    def __init__(self, google_key: str, google_cx: str, tmdb_key: str) -> None:
        self.google_key = google_key
        self.google_cx = google_cx
        self.tmdb_key = tmdb_key
        self.logger = logging.getLogger(__name__)

    def get_omdb_data(self, imdb_id: str) -> Dict:
        omdb_params = {
            'type': 'movie',
            'r': 'json',
            'tomatoes': True,
            'i': imdb_id
        }
        r = requests.get(self.omdb_url, params=omdb_params)
        omdb_data = r.json()

        if 'Error' in omdb_data:
            error_message = omdb_data.get('Error', 'OMDB API returned an error.')
            raise OMDBAPIError(error_message)

        return omdb_data

    def get_tmdb_data(self, imdb_id: str) -> Dict:
        tmdb = TMDbAPI(api_key=self.tmdb_key)
        r = tmdb.find_movie(imdb_id)
        movie_results = r.get('movie_results')
        if movie_results and len(movie_results) > 0:
            movie = movie_results[0]

            # get url for poster image for each size
            movie['poster_images'] = self.get_tmdb_images(
                base_url=tmdb.secure_image_base_url,
                image_path=movie.get('poster_path'),
                image_sizes=tmdb.configuration['images']['poster_sizes'])

            # get url for backdrop image for each size
            movie['backdrop_images'] = self.get_tmdb_images(
                base_url=tmdb.secure_image_base_url,
                image_path=movie.get('backdrop_path'),
                image_sizes=tmdb.configuration['images']['backdrop_sizes'])

            return movie
            # tmdb_id = movie_results[0]['id']
            # return tmdb.get_movie(
            #     tmdb_id, append_to_response='release_dates,videos')
        else:
            return {}

    def get_tmdb_images(self, base_url: str, image_path: str, image_sizes: List) -> Dict:
        images = {}
        if image_path:
            for size in image_sizes:
                images[size] = base_url + size + image_path
        return images

    def imdb_google_search(self, search_term: str, max_results: int=10) -> Dict:
        google_search_params = {
            'key': self.google_key,
            'cx': self.google_cx,
            'q': search_term,
            'num': max_results,
            'fields': 'items(link,title)'
        }
        r = requests.get(self.google_url, params=google_search_params)
        google_results = r.json()

        if len(google_results) == 0:
            log_message = "Google IMDb search could not find any results" \
                " for the search term: %s" % search_term
            self.logger.warning(log_message)
            return {}  # return if empty response

        if 'error' in google_results:
            error_message = google_results['error']['message']
            raise GoogleAPIError(error_message)

        return google_results

    def find_movies(self, movie_title: str, max_results: int=1) -> List:
        """
        Return IMDB ID if found using Google search
        """
        results = []
        imdb_link = re.compile(r'^https?://(?:www.)?imdb.com/title/(tt\d+)/?$')
        try:
            google_results = self.imdb_google_search(search_term=movie_title,
                                                     max_results=max_results)
            for r in google_results['items']:
                # skip results with links that are not from a movie's parent page
                # e.g. http://www.imdb.com/title/tt0133093/quotes
                link = r.get('link')
                if not imdb_link.match(link):
                    continue
                imdb_id = imdb_link.findall(link)
                movie = {
                    'omdb': self.get_omdb_data(imdb_id=imdb_id[0]) if imdb_id else None,
                    'tmdb': self.get_tmdb_data(imdb_id=imdb_id[0]) if imdb_id else None,
                    'google_result': {
                        'title': r.get('title'),
                        'imdb_id': imdb_id[0] if imdb_id else None,
                        'link': link
                    }
                }
                results.append(movie)
        except GoogleAPIError as e:
            self.logger.error(str(e))

        return results
