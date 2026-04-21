from rest_framework import serializers
from .models import Scene


class SceneListSerializer(serializers.ModelSerializer):
    """Serializer for scene list view (minimal data)."""
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Scene
        fields = [
            'id', 'movie', 'movie_title', 'title', 'scene_number',
            'scene_type', 'start_time_seconds', 'duration_seconds',
            'emotional_intensity', 'key_moments'
        ]


class SceneDetailSerializer(serializers.ModelSerializer):
    """Serializer for scene detail view (complete data)."""
    movie_title = serializers.CharField(source='movie.title', read_only=True)

    class Meta:
        model = Scene
        fields = [
            'id', 'movie', 'movie_title', 'title', 'description',
            'scene_type', 'start_time_seconds', 'end_time_seconds',
            'duration_seconds', 'location', 'characters', 'transcript',
            'scene_number', 'emotional_intensity', 'key_moments', 'tags',
            'thumbnail_url', 'video_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['duration_seconds', 'created_at', 'updated_at']


class SceneCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating scenes."""
    
    class Meta:
        model = Scene
        fields = [
            'movie', 'title', 'description', 'scene_type',
            'start_time_seconds', 'end_time_seconds', 'location',
            'characters', 'transcript', 'scene_number', 'emotional_intensity',
            'key_moments', 'tags', 'thumbnail_url', 'video_url'
        ]

    def validate(self, data):
        """Validate that end_time > start_time."""
        if data.get('end_time_seconds', 0) <= data.get('start_time_seconds', 0):
            raise serializers.ValidationError("End time must be greater than start time.")
        return data
