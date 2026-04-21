from django.urls import path
from . import views

app_name = 'analysis'

urlpatterns = [
    path('analyze/', views.analyze_scene, name='analyze_scene'),
    path('generate-scenes/', views.generate_scenes_for_movie, name='generate_scenes'),
    path('analyze-movie-scenes/', views.analyze_movie_scenes, name='analyze_movie_scenes'),
    # Additional analysis endpoints can be added here
]

