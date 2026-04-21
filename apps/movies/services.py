import os
import requests
from django.conf import settings


class ExternalMovieService:
    """Service to search and import movies using OMDb API (free)."""

    def _get_api_key(self):
        api_key = getattr(settings, 'OMDB_API_KEY', os.environ.get('OMDB_API_KEY', ''))
        if not api_key:
            raise ValueError('OMDB_API_KEY is not configured. Get a free key at http://www.omdbapi.com/apikey.aspx')
        return api_key

    def search_movies(self, query, platform=None, year=None, page=1):
        """Search for movies on OMDb API."""
        api_key = self._get_api_key()
        params = {
            'apikey': api_key,
            's': query,
            'type': 'movie',
            'page': page,
        }
        if year:
            params['y'] = year

        response = requests.get('http://www.omdbapi.com/', params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get('Response') == 'False':
            return {
                'page': page,
                'total_results': 0,
                'results': [],
                'error': data.get('Error', 'No results found')
            }

        results = []
        for item in data.get('Search', []):
            movie_info = self._build_movie_result(item)
            results.append(movie_info)

        return {
            'page': page,
            'total_results': int(data.get('totalResults', 0)),
            'results': results,
        }

    def get_movie_details(self, imdb_id):
        """Get full movie details from OMDb API."""
        api_key = self._get_api_key()
        params = {
            'apikey': api_key,
            'i': imdb_id,
            'type': 'movie',
            'plot': 'full'
        }

        response = requests.get('http://www.omdbapi.com/', params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get('Response') == 'False':
            raise ValueError(f"Movie not found: {data.get('Error')}")

        return self._build_movie_details(data)

    def _build_movie_result(self, item):
        """Build movie result from search response."""
        return {
            'imdb_id': item.get('imdbID'),
            'title': item.get('Title'),
            'year': item.get('Year'),
            'poster_url': item.get('Poster') if item.get('Poster') != 'N/A' else None,
            'type': item.get('Type'),
        }

    def _build_movie_details(self, data):
        """Build movie details from full movie response."""
        # Parse IMDb rating
        imdb_rating = None
        try:
            imdb_rating = float(data.get('imdbRating', 0))
        except (ValueError, TypeError):
            imdb_rating = None

        # Parse runtime
        duration_minutes = 0
        runtime = data.get('Runtime', '').replace(' min', '').strip()
        try:
            duration_minutes = int(runtime) if runtime else 0
        except ValueError:
            duration_minutes = 0

        return {
            'imdb_id': data.get('imdbID'),
            'title': data.get('Title'),
            'description': data.get('Plot'),
            'release_date': data.get('Released'),
            'duration_minutes': duration_minutes,
            'poster_url': data.get('Poster') if data.get('Poster') != 'N/A' else None,
            'imdb_rating': imdb_rating,
            'director': data.get('Director'),
            'actors': data.get('Actors'),
            'genre': data.get('Genre'),
            'country': data.get('Country'),
            'language': data.get('Language'),
            'budget': None,  # OMDb doesn't provide budget
            'revenue': None,  # OMDb doesn't provide revenue
            'type': data.get('Type'),
        }


external_movie_service = ExternalMovieService()
