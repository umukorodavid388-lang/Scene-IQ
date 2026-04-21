from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'scene'

router = DefaultRouter()
router.register(r'', views.SceneViewSet, basename='scene')

urlpatterns = [
    path('', include(router.urls)),
]
