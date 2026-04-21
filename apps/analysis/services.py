import re
import time
from typing import Dict, List, Any
from datetime import datetime
from .models import SceneAnalysis, AnalysisMetric


class SceneAnalyzer:
    """Service for analyzing scene text and generating analysis data."""

    # Emotional keywords and their intensity scores
    EMOTIONAL_KEYWORDS = {
        'high_intensity': {
            'words': ['scream', 'yell', 'rage', 'fury', 'terror', 'panic', 'despair', 'agony', 'horror', 'death'],
            'score': 9.0
        },
        'medium_intensity': {
            'words': ['angry', 'sad', 'happy', 'excited', 'nervous', 'worried', 'surprised', 'confused', 'jealous'],
            'score': 6.0
        },
        'low_intensity': {
            'words': ['calm', 'peaceful', 'content', 'relaxed', 'bored', 'tired', 'thoughtful'],
            'score': 3.0
        }
    }

    # Visual analysis keywords
    VISUAL_KEYWORDS = {
        'action': ['fight', 'run', 'chase', 'jump', 'crash', 'explosion', 'gunshot'],
        'dialogue': ['talk', 'speak', 'say', 'ask', 'tell', 'conversation'],
        'description': ['see', 'look', 'watch', 'view', 'appear', 'seem']
    }

    # Audio analysis patterns
    AUDIO_PATTERNS = {
        'music': r'\b(music|song|melody|tune|soundtrack)\b',
        'dialogue': r'"[^"]*"',
        'sound_effects': r'\b(bang|boom|crash|thud|whisper|scream)\b'
    }

    def analyze_text(self, text: str, analysis_types: List[str], scene_title: str = None) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on scene text.

        Args:
            text: The scene text to analyze
            analysis_types: List of analysis types to perform
            scene_title: Optional scene title

        Returns:
            Dictionary containing analysis results
        """
        start_time = time.time()
        text = text.lower().strip()
        text_length = len(text)

        analyses = []
        metrics = []

        for analysis_type in analysis_types:
            if analysis_type == 'emotional':
                analysis_data = self._analyze_emotional(text)
            elif analysis_type == 'visual':
                analysis_data = self._analyze_visual(text)
            elif analysis_type == 'audio':
                analysis_data = self._analyze_audio(text)
            elif analysis_type == 'pacing':
                analysis_data = self._analyze_pacing(text)
            elif analysis_type == 'narrative':
                analysis_data = self._analyze_narrative(text)
            elif analysis_type == 'cinematography':
                analysis_data = self._analyze_cinematography(text)
            else:
                continue

            analyses.append(analysis_data)

            # Generate metrics for this analysis
            analysis_metrics = self._generate_metrics(analysis_type, text, analysis_data)
            metrics.extend(analysis_metrics)

        processing_time = time.time() - start_time

        return {
            'scene_title': scene_title or 'Untitled Scene',
            'text_length': text_length,
            'analyses': analyses,
            'metrics': metrics,
            'processing_time_seconds': round(processing_time, 3),
            'timestamp': datetime.now()
        }

    def _analyze_emotional(self, text: str) -> Dict[str, Any]:
        """Analyze emotional content of the scene."""
        emotional_score = 5.0  # Default neutral
        emotional_indicators = []

        for intensity_level, data in self.EMOTIONAL_KEYWORDS.items():
            matches = [word for word in data['words'] if word in text]
            if matches:
                emotional_score = data['score']
                emotional_indicators.extend(matches)
                break

        # Calculate confidence based on emotional word density
        emotional_word_count = sum(len([word for word in data['words'] if word in text])
                                 for data in self.EMOTIONAL_KEYWORDS.values())
        confidence = min(0.95, emotional_word_count / max(1, len(text.split()) * 0.1))

        summary = f"Scene shows {intensity_level.replace('_', ' ')} emotional content"
        if emotional_indicators:
            summary += f" with indicators: {', '.join(emotional_indicators[:3])}"

        return {
            'analysis_type': 'emotional',
            'score': emotional_score,
            'confidence': confidence,
            'summary': summary,
            'detailed_findings': {
                'emotional_intensity': emotional_score,
                'emotional_indicators': emotional_indicators,
                'intensity_level': intensity_level
            },
            'analyzed_by': 'SceneIQ Analyzer v1.0',
            'methodology': 'Keyword-based emotional analysis',
            'data_source': 'text_input'
        }

    def _analyze_visual(self, text: str) -> Dict[str, Any]:
        """Analyze visual elements of the scene."""
        visual_elements = []
        action_score = 0
        dialogue_score = 0
        description_score = 0

        # Count visual elements
        for category, keywords in self.VISUAL_KEYWORDS.items():
            matches = [word for word in keywords if word in text]
            visual_elements.extend(matches)

            if category == 'action':
                action_score = min(10, len(matches) * 2)
            elif category == 'dialogue':
                dialogue_score = min(10, len(matches) * 1.5)
            elif category == 'description':
                description_score = min(10, len(matches) * 1.2)

        # Overall visual score based on element diversity
        visual_score = (action_score + dialogue_score + description_score) / 3
        confidence = min(0.9, len(visual_elements) / max(1, len(text.split()) * 0.05))

        summary = f"Scene contains {len(visual_elements)} visual elements"
        if visual_elements:
            summary += f" including: {', '.join(visual_elements[:3])}"

        return {
            'analysis_type': 'visual',
            'score': visual_score,
            'confidence': confidence,
            'summary': summary,
            'detailed_findings': {
                'visual_elements': visual_elements,
                'action_intensity': action_score,
                'dialogue_density': dialogue_score,
                'descriptive_elements': description_score
            },
            'analyzed_by': 'SceneIQ Analyzer v1.0',
            'methodology': 'Visual element detection and classification',
            'data_source': 'text_input'
        }

    def _analyze_audio(self, text: str) -> Dict[str, Any]:
        """Analyze audio elements of the scene."""
        audio_elements = []

        for element_type, pattern in self.AUDIO_PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                audio_elements.extend([f"{element_type}: {match[:30]}" for match in matches[:5]])

        # Score based on audio element density
        audio_score = min(10, len(audio_elements) * 1.5)
        confidence = min(0.85, len(audio_elements) / max(1, len(text.split()) * 0.03))

        summary = f"Scene contains {len(audio_elements)} audio elements"
        if audio_elements:
            summary += f" including {audio_elements[0]}"

        return {
            'analysis_type': 'audio',
            'score': audio_score,
            'confidence': confidence,
            'summary': summary,
            'detailed_findings': {
                'audio_elements': audio_elements,
                'element_types': list(set([elem.split(':')[0] for elem in audio_elements]))
            },
            'analyzed_by': 'SceneIQ Analyzer v1.0',
            'methodology': 'Pattern-based audio element detection',
            'data_source': 'text_input'
        }

    def _analyze_pacing(self, text: str) -> Dict[str, Any]:
        """Analyze pacing of the scene."""
        words = text.split()
        word_count = len(words)

        # Simple pacing analysis based on sentence structure and word count
        sentences = re.split(r'[.!?]+', text)
        avg_sentence_length = word_count / max(1, len(sentences))

        # Pacing score: shorter sentences = faster pacing
        pacing_score = max(1, min(10, 11 - avg_sentence_length / 10))

        # Action words indicate faster pacing
        action_words = ['run', 'rush', 'quickly', 'suddenly', 'fast', 'hurry']
        action_density = sum(1 for word in words if word in action_words) / max(1, word_count)

        confidence = 0.7  # Pacing analysis is more subjective

        summary = f"Scene pacing is {'fast' if pacing_score > 7 else 'moderate' if pacing_score > 4 else 'slow'}"
        summary += f" with average sentence length of {avg_sentence_length:.1f} words"

        return {
            'analysis_type': 'pacing',
            'score': pacing_score,
            'confidence': confidence,
            'summary': summary,
            'detailed_findings': {
                'word_count': word_count,
                'sentence_count': len(sentences),
                'avg_sentence_length': avg_sentence_length,
                'action_density': action_density
            },
            'analyzed_by': 'SceneIQ Analyzer v1.0',
            'methodology': 'Sentence length and action word analysis',
            'data_source': 'text_input'
        }

    def _analyze_narrative(self, text: str) -> Dict[str, Any]:
        """Analyze narrative elements of the scene."""
        # Simple narrative analysis
        has_conflict = any(word in text for word in ['fight', 'argue', 'struggle', 'problem', 'conflict'])
        has_resolution = any(word in text for word in ['resolve', 'solve', 'end', 'finish', 'conclusion'])
        has_character_development = any(word in text for word in ['learn', 'change', 'grow', 'realize', 'understand'])

        narrative_score = 5.0
        if has_conflict:
            narrative_score += 2
        if has_resolution:
            narrative_score += 1.5
        if has_character_development:
            narrative_score += 1.5

        narrative_score = min(10, narrative_score)
        confidence = 0.6  # Narrative analysis is subjective

        elements = []
        if has_conflict:
            elements.append('conflict')
        if has_resolution:
            elements.append('resolution')
        if has_character_development:
            elements.append('character development')

        summary = f"Narrative analysis shows {'strong' if narrative_score > 7 else 'moderate' if narrative_score > 4 else 'weak'} structure"
        if elements:
            summary += f" with elements: {', '.join(elements)}"

        return {
            'analysis_type': 'narrative',
            'score': narrative_score,
            'confidence': confidence,
            'summary': summary,
            'detailed_findings': {
                'narrative_elements': elements,
                'has_conflict': has_conflict,
                'has_resolution': has_resolution,
                'has_character_development': has_character_development
            },
            'analyzed_by': 'SceneIQ Analyzer v1.0',
            'methodology': 'Narrative element detection',
            'data_source': 'text_input'
        }

    def _analyze_cinematography(self, text: str) -> Dict[str, Any]:
        """Analyze cinematography elements (placeholder for future implementation)."""
        # Basic cinematography analysis based on camera-related terms
        camera_terms = ['camera', 'shot', 'angle', 'close-up', 'wide', 'pan', 'zoom', 'focus']
        lighting_terms = ['light', 'dark', 'shadow', 'bright', 'dim']

        camera_matches = [term for term in camera_terms if term in text]
        lighting_matches = [term for term in lighting_terms if term in text]

        cinematography_score = min(10, (len(camera_matches) + len(lighting_matches)) * 1.2)
        confidence = min(0.8, (len(camera_matches) + len(lighting_matches)) / max(1, len(text.split()) * 0.02))

        summary = f"Cinematography analysis detects {len(camera_matches)} camera techniques and {len(lighting_matches)} lighting elements"

        return {
            'analysis_type': 'cinematography',
            'score': cinematography_score,
            'confidence': confidence,
            'summary': summary,
            'detailed_findings': {
                'camera_techniques': camera_matches,
                'lighting_elements': lighting_matches,
                'technique_count': len(camera_matches),
                'lighting_count': len(lighting_matches)
            },
            'analyzed_by': 'SceneIQ Analyzer v1.0',
            'methodology': 'Camera and lighting term detection',
            'data_source': 'text_input'
        }

    def _generate_metrics(self, analysis_type: str, text: str, analysis_data: Dict) -> List[Dict]:
        """Generate detailed metrics for the analysis."""
        metrics = []

        if analysis_type == 'emotional':
            metrics.append({
                'metric_name': 'Emotional Intensity',
                'value': analysis_data['score'],
                'unit': 'scale',
                'description': 'Emotional intensity from 1-10',
                'threshold_min': 1.0,
                'threshold_max': 10.0
            })

        elif analysis_type == 'visual':
            findings = analysis_data['detailed_findings']
            metrics.extend([
                {
                    'metric_name': 'Action Intensity',
                    'value': findings['action_intensity'],
                    'unit': 'scale',
                    'description': 'Action sequence intensity',
                    'threshold_min': 0.0,
                    'threshold_max': 10.0
                },
                {
                    'metric_name': 'Dialogue Density',
                    'value': findings['dialogue_density'],
                    'unit': 'scale',
                    'description': 'Amount of dialogue in scene',
                    'threshold_min': 0.0,
                    'threshold_max': 10.0
                }
            ])

        elif analysis_type == 'pacing':
            findings = analysis_data['detailed_findings']
            metrics.extend([
                {
                    'metric_name': 'Average Sentence Length',
                    'value': findings['avg_sentence_length'],
                    'unit': 'words',
                    'description': 'Average words per sentence',
                    'threshold_min': 5.0,
                    'threshold_max': 25.0
                },
                {
                    'metric_name': 'Action Word Density',
                    'value': findings['action_density'] * 100,
                    'unit': 'percentage',
                    'description': 'Percentage of action-oriented words',
                    'threshold_min': 0.0,
                    'threshold_max': 20.0
                }
            ])

        return metrics


# Global analyzer instance
scene_analyzer = SceneAnalyzer()