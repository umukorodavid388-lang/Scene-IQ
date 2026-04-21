from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .serializers import AnalysisRequestSerializer, AnalysisResponseSerializer
from .services import scene_analyzer
from .models import SceneAnalysis, AnalysisMetric
from apps.movies.models import Movie
from apps.scene.models import Scene
from apps.scene.services import SceneGenerator
from apps.scene.serializers import SceneDetailSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_scene(request):
    """
    Analyze scene text and return comprehensive analysis data.

    POST /api/analysis/analyze/
    Body: {
        "text": "Scene description or transcript...",
        "scene_title": "Optional scene title",
        "analysis_types": ["emotional", "visual", "audio"]  // optional, defaults to ["emotional", "visual", "audio"]
    }

    Returns: {
        "scene_title": "Scene Title",
        "text_length": 123,
        "analyses": [...],
        "processing_time_seconds": 0.123,
        "timestamp": "2024-01-01T12:00:00Z"
    }
    """
    serializer = AnalysisRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Extract validated data
    text = serializer.validated_data['text']
    scene_title = serializer.validated_data.get('scene_title')
    analysis_types = serializer.validated_data.get('analysis_types', ['emotional', 'visual', 'audio'])

    try:
        # Perform analysis using the service
        analysis_result = scene_analyzer.analyze_text(text, analysis_types, scene_title)

        # Optionally save analysis results to database (commented out for now)
        # save_analysis_to_database(analysis_result, text)

        # Serialize the response
        response_serializer = AnalysisResponseSerializer(data=analysis_result)
        if response_serializer.is_valid():
            return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def generate_scenes_for_movie(request):
    """
    Generate scenes for a movie and optionally analyze them.

    GET /api/analysis/generate-scenes/?movie_id=1&num_scenes=3&analyze_scenes=false
    POST /api/analysis/generate-scenes/
    Body: {
        "movie_id": 1,
        "num_scenes": 3,  // optional, defaults to 3
        "analyze_scenes": true  // optional, defaults to false
    }

    Returns: {
        "movie_id": 1,
        "movie_title": "Movie Title",
        "scenes_created": 3,
        "scenes": [...],
        "analyses": [...]  // only if analyze_scenes=true
    }
    """
    # Handle both GET and POST parameters
    if request.method == 'GET':
        movie_id = request.query_params.get('movie_id')
        num_scenes = request.query_params.get('num_scenes', 3)
        analyze_scenes = request.query_params.get('analyze_scenes', 'false').lower() == 'true'
    else:  # POST
        movie_id = request.data.get('movie_id')
        num_scenes = request.data.get('num_scenes', 3)
        analyze_scenes = request.data.get('analyze_scenes', False)

    # Convert num_scenes to int if it's a string
    try:
        num_scenes = int(num_scenes)
    except (ValueError, TypeError):
        num_scenes = 3

    if not movie_id:
        return Response(
            {'error': 'movie_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response(
            {'error': 'Movie not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        # Check if scenes already exist for this movie
        existing_scenes = Scene.objects.filter(movie=movie)
        if existing_scenes.exists():
            return Response(
                {
                    'error': f'Movie already has {existing_scenes.count()} scenes. Use a different endpoint to analyze existing scenes.',
                    'existing_scenes_count': existing_scenes.count()
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate scenes for the movie
        created_scenes = SceneGenerator.generate_scenes_for_movie(movie, num_scenes)

        # Serialize scenes
        scene_serializer = SceneDetailSerializer(created_scenes, many=True)

        response_data = {
            'movie_id': movie.id,
            'movie_title': movie.title,
            'scenes_created': len(created_scenes),
            'scenes': scene_serializer.data
        }

        # Optionally analyze the scenes
        if analyze_scenes:
            analyses = []
            for scene in created_scenes:
                # Analyze the scene transcript/description
                text_to_analyze = scene.transcript or scene.description
                analysis_result = scene_analyzer.analyze_text(
                    text_to_analyze,
                    ['emotional', 'visual', 'audio', 'pacing'],
                    scene.title
                )

                # Save analysis to database
                for analysis_data in analysis_result['analyses']:
                    SceneAnalysis.objects.create(
                        scene=scene,
                        analysis_type=analysis_data['analysis_type'],
                        score=analysis_data['score'],
                        confidence=analysis_data['confidence'],
                        summary=analysis_data['summary'],
                        detailed_findings=analysis_data['detailed_findings'],
                        analyzed_by=analysis_data['analyzed_by'],
                        methodology=analysis_data['methodology'],
                        data_source=analysis_data['data_source']
                    )

                analyses.append({
                    'scene_id': scene.id,
                    'scene_title': scene.title,
                    'analysis': analysis_result
                })

            response_data['analyses'] = analyses

        return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': f'Failed to generate scenes: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def analyze_movie_scenes(request):
    """
    Analyze all existing scenes for a movie.

    GET /api/analysis/analyze-movie-scenes/?movie_id=1&analysis_types=emotional,visual,audio
    POST /api/analysis/analyze-movie-scenes/
    Body: {
        "movie_id": 1,
        "analysis_types": ["emotional", "visual", "audio"]  // optional
    }

    Returns: {
        "movie_id": 1,
        "movie_title": "Movie Title",
        "scenes_analyzed": 5,
        "analyses": [...]
    }
    """
    # Handle both GET and POST parameters
    if request.method == 'GET':
        movie_id = request.query_params.get('movie_id')
        analysis_types_str = request.query_params.get('analysis_types', 'emotional,visual,audio')
        analysis_types = [t.strip() for t in analysis_types_str.split(',')]
    else:  # POST
        movie_id = request.data.get('movie_id')
        analysis_types = request.data.get('analysis_types', ['emotional', 'visual', 'audio'])

    if not movie_id:
        return Response(
            {'error': 'movie_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return Response(
            {'error': 'Movie not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        # Get all scenes for the movie
        scenes = Scene.objects.filter(movie=movie).order_by('scene_number')

        if not scenes.exists():
            return Response(
                {'error': 'No scenes found for this movie. Generate scenes first.'},
                status=status.HTTP_404_NOT_FOUND
            )

        analyses = []
        total_scenes_analyzed = 0

        for scene in scenes:
            # Check if analysis already exists for this scene and type
            existing_analyses = SceneAnalysis.objects.filter(
                scene=scene,
                analysis_type__in=analysis_types
            )

            if existing_analyses.exists():
                # Skip scenes that are already analyzed
                continue

            # Analyze the scene
            text_to_analyze = scene.transcript or scene.description
            analysis_result = scene_analyzer.analyze_text(
                text_to_analyze,
                analysis_types,
                scene.title
            )

            # Save analysis to database
            for analysis_data in analysis_result['analyses']:
                SceneAnalysis.objects.create(
                    scene=scene,
                    analysis_type=analysis_data['analysis_type'],
                    score=analysis_data['score'],
                    confidence=analysis_data['confidence'],
                    summary=analysis_data['summary'],
                    detailed_findings=analysis_data['detailed_findings'],
                    analyzed_by=analysis_data['analyzed_by'],
                    methodology=analysis_data['methodology'],
                    data_source=analysis_data['data_source']
                )

            analyses.append({
                'scene_id': scene.id,
                'scene_title': scene.title,
                'analysis': analysis_result
            })

            total_scenes_analyzed += 1

        return Response({
            'movie_id': movie.id,
            'movie_title': movie.title,
            'scenes_analyzed': total_scenes_analyzed,
            'total_scenes': scenes.count(),
            'analyses': analyses
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    """
    Save analysis results to database (optional functionality).

    This function can be called to persist analysis results for future reference.
    Currently commented out in the main view.
    """
    # Note: This would require a Scene instance to associate with
    # For now, this is a placeholder for future implementation

    # Example implementation:
    # scene = Scene.objects.create(
    #     movie=movie_instance,
    #     title=analysis_result['scene_title'],
    #     description=original_text,
    #     scene_type='other',
    #     start_time_seconds=0,
    #     end_time_seconds=0,
    #     scene_number=1
    # )
    #
    # for analysis_data in analysis_result['analyses']:
    #     scene_analysis = SceneAnalysis.objects.create(
    #         scene=scene,
    #         analysis_type=analysis_data['analysis_type'],
    #         score=analysis_data['score'],
    #         confidence=analysis_data['confidence'],
    #         summary=analysis_data['summary'],
    #         detailed_findings=analysis_data['detailed_findings'],
    #         analyzed_by=analysis_data['analyzed_by'],
    #         methodology=analysis_data['methodology'],
    #         data_source=analysis_data['data_source']
    #     )
    #
    #     # Save metrics
    #     for metric_data in analysis_result.get('metrics', []):
    #         if metric_data.get('analysis_type') == analysis_data['analysis_type']:
    #             AnalysisMetric.objects.create(
    #                 scene_analysis=scene_analysis,
    #                 **metric_data
    #             )

    pass
