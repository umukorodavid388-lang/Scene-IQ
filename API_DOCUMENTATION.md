# SceneIQ Analysis API

## POST /api/analysis/analyze/

The core analysis endpoint that accepts scene text and returns comprehensive scene analysis data.

### Request

**Method:** `POST`  
**Content-Type:** `application/json`  
**Endpoint:** `/api/analysis/analyze/`

**Request Body:**
```json
{
  "text": "Scene description or transcript text...",
  "scene_title": "Optional scene title",
  "analysis_types": ["emotional", "visual", "audio", "pacing", "narrative", "cinematography"]
}
```

**Parameters:**
- `text` (required): The scene text to analyze
- `scene_title` (optional): Title for the scene
- `analysis_types` (optional): Array of analysis types to perform. Defaults to `["emotional", "visual", "audio"]`

**Available Analysis Types:**
- `emotional` - Analyzes emotional intensity and indicators
- `visual` - Detects visual elements and action sequences
- `audio` - Identifies audio elements and sound design
- `pacing` - Analyzes scene tempo and rhythm
- `narrative` - Evaluates story structure and elements
- `cinematography` - Detects camera techniques and lighting

### Response

**Success Response (200 OK):**
```json
{
  "scene_title": "Scene Title",
  "text_length": 245,
  "analyses": [
    {
      "analysis_type": "emotional",
      "score": 8.5,
      "confidence": 0.85,
      "summary": "Scene shows high intensity emotional content with indicators: scream, rage, terror",
      "detailed_findings": {
        "emotional_intensity": 8.5,
        "emotional_indicators": ["scream", "rage", "terror"],
        "intensity_level": "high_intensity"
      },
      "analyzed_by": "SceneIQ Analyzer v1.0",
      "methodology": "Keyword-based emotional analysis",
      "data_source": "text_input"
    }
  ],
  "metrics": [
    {
      "metric_name": "Emotional Intensity",
      "value": 8.5,
      "unit": "scale",
      "description": "Emotional intensity from 1-10",
      "threshold_min": 1.0,
      "threshold_max": 10.0
    }
  ],
  "processing_time_seconds": 0.123,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Error Response (400 Bad Request):**
```json
{
  "text": ["This field is required."]
}
```

### Analysis Types Details

#### Emotional Analysis
- **Score Range:** 1-10 (emotional intensity)
- **Detects:** Keywords indicating emotional states
- **Metrics:** Emotional intensity scale

#### Visual Analysis
- **Score Range:** 0-10 (visual element density)
- **Detects:** Action sequences, dialogue, descriptive elements
- **Metrics:** Action intensity, dialogue density

#### Audio Analysis
- **Score Range:** 0-10 (audio element density)
- **Detects:** Music, dialogue, sound effects
- **Metrics:** Audio element count by type

#### Pacing Analysis
- **Score Range:** 1-10 (pacing speed)
- **Detects:** Sentence length, action word density
- **Metrics:** Average sentence length, action density

---

## POST /api/analysis/generate-scenes/

Generate realistic scenes for a movie based on its genre and metadata.

### Request

**Method:** `POST` or `GET`  
**Content-Type:** `application/json` (for POST)  
**Endpoint:** `/api/analysis/generate-scenes/`

**POST Request Body:**
```json
{
  "movie_id": 1,
  "num_scenes": 3,
  "analyze_scenes": false
}
```

**GET Request URL:**
```
GET /api/analysis/generate-scenes/?movie_id=1&num_scenes=3&analyze_scenes=false
```

**Parameters:**
- `movie_id` (required): ID of the movie to generate scenes for
- `num_scenes` (optional): Number of scenes to generate (default: 3)
- `analyze_scenes` (optional): Whether to analyze scenes immediately (default: false)

### Response

**Success Response (201 Created):**
```json
{
  "movie_id": 1,
  "movie_title": "Inception",
  "scenes_created": 3,
  "scenes": [
    {
      "id": 1,
      "title": "Opening Action Sequence",
      "description": "High-octane opening with intense action...",
      "scene_type": "action",
      "start_time_seconds": 0,
      "end_time_seconds": 180,
      "duration_seconds": 180,
      "location": "City Street",
      "characters": "Leonardo DiCaprio, Joseph Gordon-Levitt",
      "scene_number": 1,
      "emotional_intensity": 8,
      "key_moments": true
    }
  ],
  "analyses": [] // Only if analyze_scenes=true
}
```

---

## POST /api/analysis/analyze-movie-scenes/

Analyze all scenes for a specific movie.

### Request

**Method:** `POST` or `GET`  
**Content-Type:** `application/json` (for POST)  
**Endpoint:** `/api/analysis/analyze-movie-scenes/`

**POST Request Body:**
```json
{
  "movie_id": 1,
  "analysis_types": ["emotional", "visual", "audio", "pacing"]
}
```

**GET Request URL:**
```
GET /api/analysis/analyze-movie-scenes/?movie_id=1&analysis_types=emotional,visual,audio,pacing
```

**Parameters:**
- `movie_id` (required): ID of the movie to analyze scenes for
- `analysis_types` (optional): Types of analysis to perform (default: ["emotional", "visual", "audio"])

### Response

**Success Response (200 OK):**
```json
{
  "movie_id": 1,
  "movie_title": "Inception",
  "scenes_analyzed": 3,
  "total_scenes": 3,
  "analyses": [
    {
      "scene_id": 1,
      "scene_title": "Opening Action Sequence",
      "analysis": {
        "scene_title": "Opening Action Sequence",
        "text_length": 89,
        "analyses": [
          {
            "analysis_type": "emotional",
            "score": 8.0,
            "confidence": 0.8,
            "summary": "Scene shows high intensity emotional content...",
            "detailed_findings": {
              "emotional_intensity": 8.0,
              "emotional_indicators": ["rage"],
              "intensity_level": "high_intensity"
            }
          }
        ],
        "processing_time_seconds": 0.032,
        "timestamp": "2024-01-01T12:00:00Z"
      }
    }
  ]
}
```

#### Narrative Analysis
- **Score Range:** 1-10 (narrative strength)
- **Detects:** Conflict, resolution, character development
- **Metrics:** Narrative element presence

#### Cinematography Analysis
- **Score Range:** 0-10 (technique density)
- **Detects:** Camera techniques, lighting elements
- **Metrics:** Camera technique count, lighting count

### Usage Examples

#### Basic Analysis
```bash
curl -X POST http://localhost:8000/api/analysis/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The hero screams in terror as the monster approaches. He runs through the dark forest, heart pounding."
  }'
```

#### Advanced Analysis
```bash
curl -X POST http://localhost:8000/api/analysis/analyze/ \
  -H "Content-Type: application/json" \
  -d '{
    "text": "John sits at his desk, calmly writing. The phone rings. \"Hello?\" he answers softly.",
    "scene_title": "The Call",
    "analysis_types": ["emotional", "visual", "audio", "pacing", "narrative"]
  }'
```

### Testing

Run the test script to verify the endpoint:
```bash
python test_analyze_endpoint.py
```

Make sure the Django server is running:
```bash
python manage.py runserver
```

### Implementation Notes

- **Analysis Method:** Rule-based keyword detection and pattern matching
- **Processing:** Synchronous (real-time analysis)
- **Data Storage:** Analysis results are not persisted by default (can be enabled)
- **Performance:** Typically processes 1000+ words in <0.5 seconds
- **Extensibility:** Designed to be enhanced with ML models in the future

### Future Enhancements

- Machine learning-based analysis
- Scene comparison and similarity detection
- Multi-language support
- Real-time streaming analysis
- Integration with video processing
- Advanced cinematography analysis