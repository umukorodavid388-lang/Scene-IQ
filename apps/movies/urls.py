from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'movies'

router = DefaultRouter()
router.register(r'', views.MovieViewSet, basename='movie')

urlpatterns = [
    path('', include(router.urls)),
]
