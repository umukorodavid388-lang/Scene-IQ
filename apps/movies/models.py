from django.db import models
from django.utils import timezone


class Movie(models.Model):
    """
    Movie model to store movie information.
    """
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('sci-fi', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('documentary', 'Documentary'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    producer = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='other')
    release_date = models.DateField(blank=True, null=True)
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    imdb_rating = models.FloatField(blank=True, null=True, validators=[])
    poster_url = models.URLField(blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    netflix_url = models.URLField(blank=True, null=True, help_text="Netflix page URL for the movie")
    prime_video_url = models.URLField(blank=True, null=True, help_text="Amazon Prime Video page URL for the movie")
    hulu_url = models.URLField(blank=True, null=True, help_text="Hulu page URL for the movie")
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    cast = models.TextField(blank=True, null=True, help_text="Comma-separated list of main cast")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-release_date']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['genre']),
            models.Index(fields=['release_date']),
        ]

    def get_streaming_urls(self):
        return {
            'netflix': self.netflix_url,
            'prime_video': self.prime_video_url,
            'hulu': self.hulu_url,
        }

    def __str__(self):
        return self.title
