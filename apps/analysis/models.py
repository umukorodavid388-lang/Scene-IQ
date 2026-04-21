from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.scene.models import Scene
from apps.movies.models import Movie
import json


class SceneAnalysis(models.Model):
    """
    Analysis model for scene-level analysis including emotional analysis, 
    pacing, visuals, etc.
    """
    ANALYSIS_TYPE_CHOICES = [
        ('emotional', 'Emotional Analysis'),
        ('visual', 'Visual Analysis'),
        ('audio', 'Audio Analysis'),
        ('pacing', 'Pacing Analysis'),
        ('narrative', 'Narrative Analysis'),
        ('cinematography', 'Cinematography Analysis'),
        ('other', 'Other'),
    ]

    scene = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name='analyses')
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_TYPE_CHOICES)
    
    # Score and ratings
    score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Analysis score from 0-10"
    )
    confidence = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Confidence level of the analysis (0-1)"
    )
    
    # Detailed findings
    summary = models.TextField()
    detailed_findings = models.JSONField(default=dict, blank=True)
    
    # Metadata
    analyzed_by = models.CharField(max_length=100, blank=True, null=True)
    methodology = models.CharField(max_length=255, blank=True, null=True)
    data_source = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['scene', 'analysis_type']
        indexes = [
            models.Index(fields=['scene', 'analysis_type']),
            models.Index(fields=['analysis_type']),
            models.Index(fields=['score']),
        ]

    def __str__(self):
        return f"{self.scene} - {self.analysis_type}"


class MovieAnalysis(models.Model):
    """
    High-level analysis for entire movies.
    """
    ANALYSIS_TYPE_CHOICES = [
        ('structure', 'Story Structure'),
        ('themes', 'Themes'),
        ('character', 'Character Analysis'),
        ('production', 'Production Quality'),
        ('audience', 'Audience Reception'),
        ('critical', 'Critical Analysis'),
        ('other', 'Other'),
    ]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_analyses')
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_TYPE_CHOICES)
    
    # Overall rating
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        help_text="Overall rating from 0-10"
    )
    
    # Content
    title = models.CharField(max_length=255)
    description = models.TextField()
    findings = models.JSONField(default=dict, blank=True)
    
    # Metadata
    analyst = models.CharField(max_length=100, blank=True, null=True)
    methodology = models.CharField(max_length=255, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['movie', 'analysis_type']
        indexes = [
            models.Index(fields=['movie', 'analysis_type']),
            models.Index(fields=['analysis_type']),
            models.Index(fields=['rating']),
        ]

    def __str__(self):
        return f"{self.movie.title} - {self.analysis_type}"


class AnalysisMetric(models.Model):
    """
    Detailed metrics for scene analysis with multiple key performance indicators.
    """
    scene_analysis = models.ForeignKey(SceneAnalysis, on_delete=models.CASCADE, related_name='metrics')
    
    # Metric name and value
    metric_name = models.CharField(max_length=255)
    value = models.FloatField()
    unit = models.CharField(max_length=50, blank=True, null=True)
    
    # Context
    description = models.TextField(blank=True, null=True)
    threshold_min = models.FloatField(blank=True, null=True)
    threshold_max = models.FloatField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['metric_name']
        indexes = [
            models.Index(fields=['scene_analysis', 'metric_name']),
        ]

    def __str__(self):
        return f"{self.metric_name}: {self.value} {self.unit or ''}"
