# SceneIQ API Documentation

Complete REST API for analyzing movies, scenes, and creating comprehensive scene analysis.

## Base URL
```
http://localhost:8000/api
```

---

## Endpoints Overview

### Movies API
- `GET /movies/` - List all movies
- `POST /movies/` - Create new movie (disabled; use `/movies/import_external/`)
- `GET /movies/{id}/` - Get movie details
- `PUT /movies/{id}/` - Update movie
- `DELETE /movies/{id}/` - Delete movie
- `GET /movies/by_genre/` - Filter by genre
- `GET /movies/streaming_available/` - Filter by streaming platform
- `GET /movies/top_rated/` - Get top-rated movies
- `GET /movies/{id}/streaming_urls/` - Get all streaming URLs
- `GET /movies/external_search/` - Search TMDb for movies
- `POST /movies/import_external/` - Import movie from TMDb by `tmdb_id`

### Scenes API
- `GET /scenes/` - List all scenes
- `POST /scenes/` - Create new scene
- `GET /scenes/{id}/` - Get scene details
- `PUT /scenes/{id}/` - Update scene
- `DELETE /scenes/{id}/` - Delete scene
- `GET /scenes/by_movie/` - Filter scenes by movie
- `GET /scenes/key_moments/` - Get all key moments
- `GET /scenes/by_type/` - Filter by scene type
- `GET /scenes/emotional_intensity/` - Filter by emotional intensity

### Analysis API
- `POST /analysis/analyze/` - Analyze scene text

---

## Movies API Detailed

### List Movies
```bash
GET /movies/
```

**Query Parameters:**
- `genre` - Filter by genre (action, comedy, drama, horror, sci-fi, fantasy, thriller, romance, documentary)
- `country` - Filter by country
- `language` - Filter by language
- `search` - Search by title, director, description, cast
- `ordering` - Order by field (release_date, imdb_rating, duration_minutes, title)
- `page` - Page number (default: 1, 25 results per page)

**Example:**
```bash
curl "http://localhost:8000/api/movies/?genre=action&ordering=-imdb_rating"
```

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/movies/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "The Dark Knight",
      "genre": "action",
      "release_date": "2008-07-18",
      "duration_minutes": 152,
      "imdb_rating": 9.0,
      "poster_url": "https://...",
      "streaming_urls": {
        "netflix": "https://netflix.com/...",
        "prime_video": "https://prime.amazon.com/...",
        "hulu": null
      }
    }
  ]
}
```

### Get Top Rated Movies
```bash
GET /movies/top_rated/?limit=10
```

**Response:** Returns top 10 rated movies

### Get Movies by Streaming Platform
```bash
GET /movies/streaming_available/?platform=netflix
```

**Supported Platforms:** netflix, prime, hulu

**Response:** Returns movies available on Netflix

### Get All Streaming URLs for a Movie
```bash
GET /movies/{id}/streaming_urls/
```

**Response:**
```json
{
  "netflix": "https://www.netflix.com/title/...",
  "prime_video": "https://www.primevideo.com/detail/...",
  "hulu": null
}
```

### Create Movie
Manual movie creation through `POST /movies/` is disabled in this project. Use the OMDb import endpoint instead.

### Search Movies on OMDb
```bash
GET /movies/external_search/?q=inception&year=2010
```

**Query Parameters:**
- `q` - Search query text (required)
- `year` - Optional movie release year
- `platform` - Optional platform filter parameter (netflix, prime, hulu)

**Example:**
```bash
curl "http://localhost:8000/api/movies/external_search/?q=inception&year=2010"
```

**Response:**
```json
{
  "page": 1,
  "total_results": 100,
  "results": [
    {
      "imdb_id": "tt1375666",
      "title": "Inception",
      "year": "2010",
      "poster_url": "https://m.media-amazon.com/images/M/...",
      "type": "movie"
    }
  ]
}
```

### Import Movie from OMDb
```bash
POST /movies/import_external/
Content-Type: application/json

{
  "imdb_id": "tt1375666"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/movies/import_external/" \
  -H "Content-Type: application/json" \
  -d '{"imdb_id": "tt1375666"}'
```

**Response:**
```json
{
  "id": 123,
  "title": "Inception",
  "description": "A skilled thief...",
  "director": "Christopher Nolan",
  "genre": "action",
  "release_date": "2010-07-16",
  "duration_minutes": 148,
  "imdb_rating": 8.8,
  "poster_url": "https://m.media-amazon.com/images/M/...",
  "trailer_url": null,
  "budget": null,
  "revenue": null,
  "language": null,
  "country": null,
  "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page",
  "streaming_urls": {
    "netflix": null,
    "prime_video": null,
    "hulu": null
  }
}
```

---

## Scenes API Detailed

### List Scenes
```bash
GET /scenes/
```

**Query Parameters:**
- `movie` - Filter by movie ID
- `scene_type` - Filter by type (action, dialogue, montage, transition, exposition, climax, other)
- `key_moments` - Filter by key moments (true/false)
- `search` - Search by title, description, location, characters
- `ordering` - Order by field (scene_number, emotional_intensity, start_time_seconds)

**Example:**
```bash
curl "http://localhost:8000/api/scenes/?movie=1&scene_type=action&ordering=-emotional_intensity"
```

### Get Scenes by Movie
```bash
GET /scenes/by_movie/?movie_id=1
```

### Get Key Moments
```bash
GET /scenes/key_moments/
```

**Response:** Returns all scenes marked as key moments across all movies

### Filter by Emotional Intensity
```bash
GET /scenes/emotional_intensity/?min=7&max=10
```

**Response:** Returns scenes with emotional intensity between 7 and 10

### Create Scene
```bash
POST /scenes/
Content-Type: application/json

{
  "movie": 1,
  "title": "Scene Title",
  "description": "Scene description",
  "scene_type": "action",
  "start_time_seconds": 0,
  "end_time_seconds": 100,
  "location": "New York City",
  "characters": "John, Jane",
  "transcript": "Dialogue text...",
  "scene_number": 1,
  "emotional_intensity": 8,
  "key_moments": true,
  "tags": "action, chase, climax",
  "thumbnail_url": "https://...",
  "video_url": "https://..."
}
```

---

## Analysis API

### Analyze Scene Text
```bash
POST /analysis/analyze/
Content-Type: application/json

{
  "text": "The hero screams in terror as the monster approaches...",
  "scene_title": "Confrontation",
  "analysis_types": ["emotional", "visual", "audio", "pacing", "narrative", "cinematography"]
}
```

**Query Parameters:**
- `text` (required) - Scene text to analyze
- `scene_title` (optional) - Title for the scene
- `analysis_types` (optional) - Array of analysis types (default: ["emotional", "visual", "audio"])

**Analysis Types:**
- `emotional` - Emotional intensity and indicators
- `visual` - Visual elements and action sequences
- `audio` - Audio elements and sound design
- `pacing` - Scene tempo and rhythm
- `narrative` - Story structure and elements
- `cinematography` - Camera techniques and lighting

**Response:**
```json
{
  "scene_title": "Confrontation",
  "text_length": 245,
  "analyses": [
    {
      "id": 1,
      "analysis_type": "emotional",
      "score": 8.5,
      "confidence": 0.85,
      "summary": "Scene shows high intensity emotional content with indicators: scream, terror",
      "detailed_findings": {
        "emotional_intensity": 8.5,
        "emotional_indicators": ["scream", "terror"],
        "intensity_level": "high_intensity"
      },
      "analyzed_by": "SceneIQ Analyzer v1.0",
      "methodology": "Keyword-based emotional analysis",
      "data_source": "text_input",
      "created_at": "2024-01-01T12:00:00Z",
      "metrics": []
    }
  ],
  "metrics": [],
  "processing_time_seconds": 0.045,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Generate Scenes for Movie
```bash
POST /analysis/generate-scenes/
Content-Type: application/json

{
  "movie_id": 1,
  "num_scenes": 3,
  "analyze_scenes": false
}
```

Or via GET:
```bash
GET /analysis/generate-scenes/?movie_id=1&num_scenes=3&analyze_scenes=false
```

**Parameters:**
- `movie_id` (required) - ID of the movie to generate scenes for
- `num_scenes` (optional) - Number of scenes to generate (default: 3)
- `analyze_scenes` (optional) - Whether to analyze the generated scenes immediately (default: false)

**Response:**
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
      "transcript": "The hero bursts through the door...",
      "scene_number": 1,
      "emotional_intensity": 8,
      "key_moments": true,
      "tags": "action, action",
      "thumbnail_url": null,
      "video_url": null,
      "created_at": "2024-01-01T12:00:00Z",
      "updated_at": "2024-01-01T12:00:00Z"
    }
  ],
  "analyses": []  // Only present if analyze_scenes=true
}
```

### Analyze Movie Scenes
```bash
POST /analysis/analyze-movie-scenes/
Content-Type: application/json

{
  "movie_id": 1,
  "analysis_types": ["emotional", "visual", "audio", "pacing"]
}
```

Or via GET:
```bash
GET /analysis/analyze-movie-scenes/?movie_id=1&analysis_types=emotional,visual,audio,pacing
```

**Parameters:**
- `movie_id` (required) - ID of the movie whose scenes to analyze
- `analysis_types` (optional) - Array of analysis types to perform (default: ["emotional", "visual", "audio"])

**Response:**
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
            },
            "analyzed_by": "SceneIQ Analyzer v1.0",
            "methodology": "Keyword-based emotional analysis",
            "data_source": "text_input"
          }
        ],
        "metrics": [],
        "processing_time_seconds": 0.032,
        "timestamp": "2024-01-01T12:00:00Z"
      }
    }
  ]
}
```

---

## Search API

### Global Search
```bash
GET /search/search/?q=keyword&type=all&limit=10
```

**Query Parameters:**
- `q` (required) - Search query
- `type` (optional) - Search type (all, movie, scene, analysis) - default: all
- `limit` (optional) - Maximum results per type - default: 10

**Example:**
```bash
curl "http://localhost:8000/api/search/search/?q=dark+knight&type=movie&limit=5"
```

**Response:**
```json
{
  "query": "dark knight",
  "search_type": "movie",
  "results": {
    "movies": [
      {
        "id": 1,
        "title": "The Dark Knight",
        "genre": "action",
        "release_date": "2008-07-18",
        "duration_minutes": 152,
        "imdb_rating": 9.0,
        "poster_url": "https://...",
        "streaming_urls": {
          "netflix": "...",
          "prime_video": "...",
          "hulu": null
        }
      }
    ],
    "movie_count": 1
  }
}
```

### Advanced Search
```bash
GET /search/advanced/?q=query&search_in=movie&genre=action&director=Nolan&min_rating=8.0&year_from=2000&year_to=2024
```

**Movie Filters:**
- `genre` - Filter by genre
- `director` - Filter by director name
- `min_rating` - Minimum IMDb rating
- `year_from` - Movies from year (inclusive)
- `year_to` - Movies to year (inclusive)

**Scene Filters:**
- `movie_id` - Specific movie
- `scene_type` - Type of scene
- `min_intensity` - Minimum emotional intensity (1-10)
- `max_intensity` - Maximum emotional intensity (1-10)
- `key_moments` - true/false

**Example:**
```bash
curl "http://localhost:8000/api/search/advanced/?search_in=scene&scene_type=action&min_intensity=7&max_intensity=10"
```

---

## Common Query Examples

### Get all action movies from 2020 with rating > 8
```bash
GET /movies/?genre=action&year_from=2020&min_rating=8&ordering=-imdb_rating
```

### Get all scenes from a specific movie that are key moments
```bash
GET /scenes/by_movie/?movie_id=1
GET /scenes/?movie=1&key_moments=true
```

### Search for intense emotional scenes
```bash
GET /scenes/emotional_intensity/?min=8&max=10
```

### Analyze a scene and get comprehensive analysis
```bash
POST /analysis/analyze/
{
  "text": "Scene text here...",
  "analysis_types": ["emotional", "visual", "pacing"]
}
```

### Find all Drake movies available on Netflix
```bash
GET /search/search/?q=drake&type=movie
GET /movies/streaming_available/?platform=netflix
```

---

## Error Handling

### Invalid Query
```json
{
  "error": "Please provide a search query parameter (q)"
}
```

### Not Found
```json
{
  "detail": "Not found."
}
```

### Validation Error
```json
{
  "field_name": ["Error message"],
  "another_field": ["Another error message"]
}
```

---

## Pagination

Default page size: 25 items

```bash
GET /movies/?page=1
GET /movies/?page=2
```

**Response includes:**
- `count` - Total number of items
- `next` - URL to next page
- `previous` - URL to previous page
- `results` - Array of items

---

## Testing

Run the provided test script:
```bash
python test_analyze_endpoint.py
```

Or use curl/Postman to test endpoints directly.

---

## Notes

- All timestamps are in UTC
- Scores are on a 0-10 scale (or specified range)
- Confidence levels are 0-1 (0% to 100%)
- All URLs support filtering and searching
- Results are paginated (25 per page by default)
- Analysis endpoints return results in real-time
