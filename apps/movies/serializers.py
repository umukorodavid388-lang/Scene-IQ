from rest_framework import serializers
from .models import Movie


class MovieListSerializer(serializers.ModelSerializer):
    """Serializer for movie list view (minimal data)."""
    streaming_urls = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'genre', 'release_date', 'duration_minutes',
            'imdb_rating', 'poster_url', 'streaming_urls'
        ]

    def get_streaming_urls(self, obj):
        return obj.get_streaming_urls()


class MovieDetailSerializer(serializers.ModelSerializer):
    """Serializer for movie detail view (complete data)."""
    streaming_urls = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'description', 'director', 'producer', 'genre',
            'release_date', 'duration_minutes', 'imdb_rating', 'poster_url',
            'trailer_url', 'netflix_url', 'prime_video_url', 'hulu_url',
            'budget', 'revenue', 'language', 'country', 'cast',
            'streaming_urls', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_streaming_urls(self, obj):
        return obj.get_streaming_urls()


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating movies."""
    
    class Meta:
        model = Movie
        fields = [
            'title', 'description', 'director', 'producer', 'genre',
            'release_date', 'duration_minutes', 'imdb_rating', 'poster_url',
            'trailer_url', 'netflix_url', 'prime_video_url', 'hulu_url',
            'budget', 'revenue', 'language', 'country', 'cast'
        ]

    def validate_title(self, value):
        """Check if title is unique (except on update)."""
        instance = self.instance
        if Movie.objects.filter(title=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("A movie with this title already exists.")
        return value


class ExternalMovieSerializer(serializers.Serializer):
    """Serializer for external movie search results."""
    tmdb_id = serializers.IntegerField()
    title = serializers.CharField()
    overview = serializers.CharField(required=False, allow_blank=True)
    release_date = serializers.DateField(required=False, allow_null=True)
    duration_minutes = serializers.IntegerField(required=False)
    poster_url = serializers.URLField(required=False, allow_null=True)
    backdrop_url = serializers.URLField(required=False, allow_null=True)
    popularity = serializers.FloatField(required=False)
    vote_average = serializers.FloatField(required=False)
    vote_count = serializers.IntegerField(required=False)
    platforms = serializers.ListField(child=serializers.CharField(), required=False)
