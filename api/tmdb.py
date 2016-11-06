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
