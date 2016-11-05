import requests


class TMDbAPI(object):
    api_url = 'http://api.themoviedb.org/3/'

    def __init__(self, api_key):
        self.api_key = api_key
        r = self.make_request(resource='configuration')
        self.configuration = r
        self.image_base_url = r['images']['base_url']
        self.secure_image_base_url = r['images']['secure_base_url']

    def get_image(self, image_path, size='w500'):
        url = self.image_base_url + size + image_path
        r = requests.get(url)
        if r.status_code == 200:
            return r.content
        else:
            return ''

    def make_request(self, resource='', **kwargs):
        params = {'api_key': self.api_key}
        params.update(kwargs)
        url = self.api_url + resource
        r = requests.get(url, params=params)
        return r.json()

    def search_movie(self, title, year):
        resource = 'search/movie'
        results = self.make_request(resource=resource, query=title, year=year)
        return results

    def find_movie(self, external_id, external_source='imdb_id'):
        resource = 'find/{external_id}'.format(external_id=external_id)
        results = self.make_request(resource=resource,
                                    external_source=external_source)
        return results

    def get_movie(self, movie_id, append_to_response=None):
        resource = 'movie/{id}'.format(id=movie_id)
        if append_to_response:
            results = self.make_request(resource=resource,
                                        append_to_response=append_to_response)
        else:
            results = self.make_request(resource=resource)
        return results

    def list_genres(self):
        resource = 'genre/movie/list'
        results = self.make_request(resource=resource)
        return results


# class MovieNotFound(Exception):
#     pass


# class TMDbMovie(object):
#     MovieNotFound = MovieNotFound

#     def __init__(self, imdb_id=None):
#         self.api = MovieAPI('')
#         self._data = {}
#         self._cached_data = {}
#         r = self.api.find_movie(imdb_id)
#         movie_results = r.get('movie_results')
#         if movie_results and len(movie_results) > 0:
#             tmdb_id = movie_results[0]['id']
#             self._data = self.api.get_movie(
#                 tmdb_id, append_to_response='release_dates,videos')
#         else:
#             raise MovieNotFound("TMDb could not find movie with IMDB ID (%s)"
#                                 % imdb_id)

#     @property
#     def data(self):
#         if self._cached_data:
#             return self._cached_data
#         data = {
#             'title': self._data.get('title'),
#             'overview': self._data.get('overview'),
#             'tmdb_id': self._data.get('id'),
#             'original_title': self._data.get('original_title'),
#             'original_language': self._data.get('original_language'),
#             'run_time': self._data.get('runtime'),
#             'homepage': self._data.get('homepage'),
#             'tag_line': self._data.get('tagline'),
#             'youtube_trailer_id': self.get_youtube_key(),
#             'release_date': self.get_release_date('AU'),
#             'poster_image': self.get_poster_image(size='original'),
#             'backdrop_image': self.get_backdrop_image(),
#         }
#         self._cached_data = data
#         return data

#     @property
#     def genres(self):
#         return self._data.get('genres')

#     def get_youtube_key(self):
#         videos = self._data.get('videos')
#         if videos and len(videos.get('results', [])) > 0:
#             for video in videos['results']:
#                 if (video.get('type') == 'Trailer' and
#                         video.get('site') == 'YouTube'):
#                     return video.get('key')
#         return

#     def get_release_date(self, country_code='AU'):
#         release_dates = self._data.get('release_dates')
#         if release_dates and len(release_dates.get('results', [])) > 0:
#             for date in self._data['release_dates']['results']:
#                 if date['iso_3166_1'] == country_code:
#                     release_date = date['release_dates'][0]['release_date']
#                     return parse(release_date)
#                 else:
#                     return self._data.get('release_date')
#         return

#     def get_poster_image(self, size='w500'):
#         poster_path = self._data.get('poster_path')
#         if poster_path:
#             poster_name = poster_path.split('/')[-1]
#             return ContentFile(self.api.get_image(poster_path, size=size),
#                                name=poster_name)
#         return

#     def get_backdrop_image(self, size='w780'):
#         backdrop_path = self._data.get('backdrop_path')
#         if backdrop_path:
#             backdrop_name = backdrop_path.split('/')[-1]
#             return ContentFile(self.api.get_image(backdrop_path, size=size),
#                                name=backdrop_name)
#         return

    # def get_genre_list(self):
    #     genres = self._data.get('genres')
    #     genre_list = []
    #     if genres and len(genres) > 0:
    #         for genre in genres:
    #             genre_obj, created = Genre.objects.get_or_create(
    #                 tmdb_id=genre['id'])
    #             genre_list.append(genre_obj)
    #     return genre_list
