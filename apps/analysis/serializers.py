from rest_framework import serializers
from .models import SceneAnalysis, AnalysisMetric


class AnalysisRequestSerializer(serializers.Serializer):
    """Serializer for analysis request data."""
    text = serializers.CharField(required=True, help_text="Scene text to analyze")
    scene_title = serializers.CharField(required=False, max_length=255, help_text="Optional scene title")
    analysis_types = serializers.ListField(
        child=serializers.ChoiceField(choices=[
            'emotional', 'visual', 'audio', 'pacing', 'narrative', 'cinematography'
        ]),
        required=False,
        default=['emotional', 'visual', 'audio'],
        help_text="Types of analysis to perform"
    )


class AnalysisMetricSerializer(serializers.ModelSerializer):
    """Serializer for analysis metrics."""
    class Meta:
        model = AnalysisMetric
        fields = ['metric_name', 'value', 'unit', 'description', 'threshold_min', 'threshold_max']


class SceneAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for scene analysis response."""
    metrics = AnalysisMetricSerializer(many=True, read_only=True)

    class Meta:
        model = SceneAnalysis
        fields = [
            'id', 'analysis_type', 'score', 'confidence', 'summary',
            'detailed_findings', 'analyzed_by', 'methodology', 'data_source',
            'created_at', 'metrics'
        ]
        read_only_fields = ['id', 'created_at']


class AnalysisResponseSerializer(serializers.Serializer):
    """Serializer for complete analysis response."""
    scene_title = serializers.CharField()
    text_length = serializers.IntegerField()
    analyses = SceneAnalysisSerializer(many=True)
    processing_time_seconds = serializers.FloatField()
    timestamp = serializers.DateTimeField()