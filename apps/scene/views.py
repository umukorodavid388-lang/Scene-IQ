from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Scene
from .serializers import SceneListSerializer, SceneDetailSerializer, SceneCreateUpdateSerializer


class SceneViewSet(viewsets.ModelViewSet):
    """
    API endpoint for scenes.
    
    Provides CRUD operations and filtering by movie, scene type, and key moments.
    """
    queryset = Scene.objects.all().order_by('movie', 'scene_number')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['movie', 'scene_type', 'key_moments']
    search_fields = ['title', 'description', 'location', 'characters']
    ordering_fields = ['scene_number', 'emotional_intensity', 'start_time_seconds']

    def get_serializer_class(self):
        """Use different serializers based on action."""
        if self.action == 'list':
            return SceneListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SceneCreateUpdateSerializer
        return SceneDetailSerializer

    @action(detail=False, methods=['get'])
    def by_movie(self, request):
        """Get all scenes for a specific movie."""
        movie_id = request.query_params.get('movie_id')
        if not movie_id:
            return Response(
                {'error': 'Please provide a movie_id parameter'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        scenes = self.queryset.filter(movie_id=movie_id)
        serializer = self.get_serializer(scenes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def key_moments(self, request):
        """Get all key moments (important scenes) across movies."""
        scenes = self.queryset.filter(key_moments=True)
        serializer = self.get_serializer(scenes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get scenes filtered by scene type."""
        scene_type = request.query_params.get('type')
        if not scene_type:
            return Response(
                {'error': 'Please provide a type parameter'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        scenes = self.queryset.filter(scene_type=scene_type)
        serializer = self.get_serializer(scenes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def emotional_intensity(self, request):
        """Get scenes filtered by emotional intensity."""
        min_intensity = request.query_params.get('min', 1)
        max_intensity = request.query_params.get('max', 10)
        
        try:
            min_intensity = int(min_intensity)
            max_intensity = int(max_intensity)
        except ValueError:
            return Response(
                {'error': 'min and max must be integers'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        scenes = self.queryset.filter(
            emotional_intensity__gte=min_intensity,
            emotional_intensity__lte=max_intensity
        )
        serializer = self.get_serializer(scenes, many=True)
        return Response(serializer.data)

