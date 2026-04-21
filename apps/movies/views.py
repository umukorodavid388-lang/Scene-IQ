import requests
from django.conf import settings
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from .models import Movie
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    MovieCreateUpdateSerializer,
)
from .services import external_movie_service


class MovieViewSet(viewsets.ModelViewSet):
    """
    API endpoint for movies.
    
    Provides CRUD operations and filtering by genre, year, and rating.
    """
    queryset = Movie.objects.all().order_by('-release_date')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genre', 'country', 'language']
    search_fields = ['title', 'director', 'description', 'cast']
    ordering_fields = ['release_date', 'imdb_rating', 'duration_minutes', 'title']

    def list(self, request, *args, **kwargs):
        """List movies from external API instead of database."""
        query = request.query_params.get('q', 'movie')  # default search query
        platform = request.query_params.get('platform', '').lower()
        year = request.query_params.get('year')
        page = request.query_params.get('page', 1)

        if year:
            try:
                year = int(year)
            except ValueError:
                year = None

        try:
            page = int(page)
        except ValueError:
            page = 1

        try:
            result = external_movie_service.search_movies(query, platform=platform or None, year=year, page=page)
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.RequestException as exc:
            return Response({'error': f'External API error: {str(exc)}'}, status=status.HTTP_502_BAD_GATEWAY)

        # Automatically save movies to database
        for item in result['results']:
            if not Movie.objects.filter(title=item['title']).exists():
                try:
                    details = external_movie_service.get_movie_details(item['imdb_id'])
                    
                    # Parse release date
                    release_date = None
                    release_date_str = details.get('release_date')
                    if release_date_str and release_date_str != 'N/A':
                        try:
                            release_date = datetime.strptime(release_date_str, '%d %b %Y').date()
                        except ValueError:
                            release_date = None
                    
                    Movie.objects.create(
                        title=details['title'],
                        description=details.get('description', ''),
                        director=details.get('director'),
                        genre=details.get('genre', 'other').split(',')[0].strip() if details.get('genre') else 'other',
                        release_date=release_date,
                        duration_minutes=details.get('duration_minutes', 0),
                        imdb_rating=details.get('imdb_rating'),
                        poster_url=details.get('poster_url'),
                        language=details.get('language'),
                        country=details.get('country'),
                        cast=details.get('cast'),
                    )
                except Exception as e:
                    # Skip if error saving, but could log e
                    pass

        return Response(result)

    def get_serializer_class(self):
        """Use different serializers based on action."""
        if self.action == 'list':
            return MovieListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MovieCreateUpdateSerializer
        return MovieDetailSerializer

    @action(detail=False, methods=['get'])
    def by_genre(self, request):
        """Get movies filtered by genre."""
        genre = request.query_params.get('genre')
        if not genre:
            return Response(
                {'error': 'Please provide a genre parameter'},
                status=status.HTTP_400_BAD_REQUEST
            )
        movies = self.queryset.filter(genre=genre)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def streaming_available(self, request):
        """Get movies available on specific streaming platform."""
        platform = request.query_params.get('platform', '').lower()
        
        platform_field_map = {
            'netflix': 'netflix_url__isnull',
            'prime': 'prime_video_url__isnull',
            'hulu': 'hulu_url__isnull',
        }
        
        if platform not in platform_field_map:
            return Response(
                {'error': f'Platform must be one of: {", ".join(platform_field_map.keys())}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        filter_kwargs = {platform_field_map[platform]: False}
        movies = self.queryset.filter(**filter_kwargs)
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """Get top-rated movies."""
        limit = request.query_params.get('limit', 10)
        try:
            limit = int(limit)
        except ValueError:
            limit = 10
        
        movies = self.queryset.filter(imdb_rating__isnull=False).order_by('-imdb_rating')[:limit]
        serializer = self.get_serializer(movies, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def external_search(self, request):
        """Search for movies using an external film API."""
        query = request.query_params.get('q', '').strip()
        platform = request.query_params.get('platform', '').lower()
        year = request.query_params.get('year')

        if not query:
            return Response(
                {'error': 'Please provide a search query parameter (q)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if platform and platform not in ['netflix', 'prime', 'hulu']:
            return Response(
                {'error': 'Platform must be one of: netflix, prime, hulu'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if year:
                year = int(year)
        except ValueError:
            year = None

        try:
            result = external_movie_service.search_movies(query, platform=platform or None, year=year)
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.RequestException as exc:
            return Response({'error': f'External API error: {str(exc)}'}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(result)

    def create(self, request, *args, **kwargs):
        """Disable manual movie creation through the public API."""
        return Response(
            {'error': 'Manual movie creation is disabled. Use /api/movies/import_external/ with imdb_id to import movies from OMDb.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    @action(detail=False, methods=['post'])
    def import_external(self, request):
        """Import a movie from OMDb API into the local database."""
        imdb_id = request.data.get('imdb_id')
        if not imdb_id:
            return Response(
                {'error': 'Please provide imdb_id (e.g., "tt0111161") in the request body.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            external_movie = external_movie_service.get_movie_details(imdb_id)
        except ValueError as exc:
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.RequestException as exc:
            return Response({'error': f'External API error: {str(exc)}'}, status=status.HTTP_502_BAD_GATEWAY)

        data = {
            'title': external_movie['title'],
            'description': external_movie.get('description', ''),
            'director': external_movie.get('director') or request.data.get('director'),
            'producer': request.data.get('producer'),
            'genre': external_movie.get('genre', 'other').split(',')[0].strip() if external_movie.get('genre') else 'other',
            'release_date': external_movie.get('release_date'),
            'duration_minutes': external_movie.get('duration_minutes') or 0,
            'imdb_rating': external_movie.get('imdb_rating'),
            'poster_url': external_movie.get('poster_url'),
            'trailer_url': request.data.get('trailer_url'),
            'netflix_url': request.data.get('netflix_url'),
            'prime_video_url': request.data.get('prime_video_url'),
            'hulu_url': request.data.get('hulu_url'),
            'budget': request.data.get('budget'),
            'revenue': request.data.get('revenue'),
            'language': external_movie.get('language') or request.data.get('language'),
            'country': external_movie.get('country') or request.data.get('country'),
            'cast': external_movie.get('actors') or request.data.get('cast'),
        }

        serializer = MovieCreateUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        movie = serializer.save()
        return Response(MovieDetailSerializer(movie).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def streaming_urls(self, request, pk=None):
        """Get all streaming URLs for a specific movie."""
        movie = self.get_object()
        return Response(movie.get_streaming_urls())

