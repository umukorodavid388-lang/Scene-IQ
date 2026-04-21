from django.contrib import admin
from .models import SceneAnalysis, MovieAnalysis, AnalysisMetric


class AnalysisMetricInline(admin.TabularInline):
    model = AnalysisMetric
    extra = 1
    fields = ('metric_name', 'value', 'unit', 'description')


@admin.register(SceneAnalysis)
class SceneAnalysisAdmin(admin.ModelAdmin):
    list_display = ('scene', 'analysis_type', 'score', 'confidence', 'created_at')
    search_fields = ('scene__title', 'analysis_type')
    list_filter = ('analysis_type', 'score', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [AnalysisMetricInline]
    
    fieldsets = (
        ('Scene & Analysis Type', {
            'fields': ('scene', 'analysis_type')
        }),
        ('Scoring', {
            'fields': ('score', 'confidence')
        }),
        ('Content', {
            'fields': ('summary', 'detailed_findings')
        }),
        ('Metadata', {
            'fields': ('analyzed_by', 'methodology', 'data_source')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MovieAnalysis)
class MovieAnalysisAdmin(admin.ModelAdmin):
    list_display = ('movie', 'analysis_type', 'title', 'rating', 'created_at')
    search_fields = ('movie__title', 'analysis_type', 'title')
    list_filter = ('analysis_type', 'rating', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Movie & Analysis', {
            'fields': ('movie', 'analysis_type', 'title')
        }),
        ('Rating & Content', {
            'fields': ('rating', 'description', 'findings')
        }),
        ('Metadata', {
            'fields': ('analyst', 'methodology')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AnalysisMetric)
class AnalysisMetricAdmin(admin.ModelAdmin):
    list_display = ('metric_name', 'scene_analysis', 'value', 'unit')
    search_fields = ('metric_name', 'scene_analysis__scene__title')
    list_filter = ('metric_name', 'unit')
    
    fieldsets = (
        ('Metric Information', {
            'fields': ('scene_analysis', 'metric_name', 'value', 'unit')
        }),
        ('Details', {
            'fields': ('description', 'threshold_min', 'threshold_max')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
