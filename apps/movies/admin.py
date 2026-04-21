from django.contrib import admin
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'genre', 'release_date', 'duration_minutes', 'imdb_rating')
    search_fields = ('title', 'director', 'genre')
    list_filter = ('genre', 'release_date', 'country')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'genre')
        }),
        ('Credits', {
            'fields': ('director', 'producer', 'cast')
        }),
        ('Details', {
            'fields': ('release_date', 'duration_minutes', 'language', 'country')
        }),
        ('Media & Links', {
            'fields': ('poster_url', 'trailer_url', 'netflix_url', 'prime_video_url', 'hulu_url')
        }),
        ('Ratings & Revenue', {
            'fields': ('imdb_rating', 'budget', 'revenue')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
