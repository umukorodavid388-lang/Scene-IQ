from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.movies.models import Movie


class Scene(models.Model):
    """
    Scene model to store individual scenes from movies.
    """
    SCENE_TYPE_CHOICES = [
        ('action', 'Action'),
        ('dialogue', 'Dialogue'),
        ('montage', 'Montage'),
        ('transition', 'Transition'),
        ('exposition', 'Exposition'),
        ('climax', 'Climax'),
        ('other', 'Other'),
    ]

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='scenes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    scene_type = models.CharField(max_length=50, choices=SCENE_TYPE_CHOICES, default='other')
    
    # Timing information
    start_time_seconds = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Scene start time in seconds"
    )
    end_time_seconds = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Scene end time in seconds"
    )
    duration_seconds = models.IntegerField(
        help_text="Scene duration in seconds",
        editable=False
    )
    
    # Content information
    location = models.CharField(max_length=255, blank=True, null=True)
    characters = models.TextField(blank=True, null=True, help_text="Comma-separated list of characters")
    transcript = models.TextField(blank=True, null=True)
    
    # Metadata
    scene_number = models.IntegerField(help_text="Sequential scene number in the movie")
    emotional_intensity = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Emotional intensity from 1-10"
    )
    key_moments = models.BooleanField(default=False, help_text="Whether this is a key/notable moment")
    tags = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Comma-separated tags for categorization"
    )
    
    # Media
    thumbnail_url = models.URLField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['movie', 'scene_number']
        unique_together = ['movie', 'scene_number']
        indexes = [
            models.Index(fields=['movie', 'scene_number']),
            models.Index(fields=['scene_type']),
            models.Index(fields=['key_moments']),
        ]

    def save(self, *args, **kwargs):
        """Automatically calculate duration when saved."""
        self.duration_seconds = self.end_time_seconds - self.start_time_seconds
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie.title} - Scene {self.scene_number}: {self.title}"
