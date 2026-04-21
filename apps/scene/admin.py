from django.contrib import admin
from .models import Scene


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'scene_number', 'scene_type', 'start_time_seconds', 'duration_seconds', 'key_moments')
    search_fields = ('title', 'movie__title', 'location', 'characters')
    list_filter = ('scene_type', 'key_moments', 'movie')
    readonly_fields = ('created_at', 'updated_at', 'duration_seconds')
    
    fieldsets = (
        ('Scene Information', {
            'fields': ('movie', 'scene_number', 'title', 'description', 'scene_type')
        }),
        ('Timing', {
            'fields': ('start_time_seconds', 'end_time_seconds', 'duration_seconds')
        }),
        ('Content Details', {
            'fields': ('location', 'characters', 'transcript')
        }),
        ('Analysis & Tags', {
            'fields': ('emotional_intensity', 'key_moments', 'tags')
        }),
        ('Media', {
            'fields': ('thumbnail_url', 'video_url')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
