# SceneIQ Database Schema

## Overview
The database schema has been successfully set up with four main apps: Movies, Scene, Analysis, and Search. The schema supports comprehensive scene analysis, including movies, individual scenes, and various analysis types.

---

## Database Models

### 1. **Movie Model** (`apps.movies.models.Movie`)
Stores information about movies.

**Fields:**
- `id` (BigAutoField, Primary Key)
- `title` (CharField, max_length=255, UNIQUE, indexed)
- `description` (TextField, optional)
- `director` (CharField, max_length=255, optional)
- `producer` (CharField, max_length=255, optional)
- `genre` (CharField, choices: action, comedy, drama, horror, sci-fi, fantasy, thriller, romance, documentary, other)
- `release_date` (DateField, optional)
- `duration_minutes` (IntegerField)
- `imdb_rating` (FloatField, optional)
- `poster_url` (URLField, optional)
- `trailer_url` (URLField, optional)
- `budget` (DecimalField, max_digits=12, decimal_places=2)
- `revenue` (DecimalField, max_digits=12, decimal_places=2)
- `language` (CharField, max_length=50, optional)
- `country` (CharField, max_length=100, optional)
- `cast` (TextField, optional)
- `created_at` (DateTimeField, auto_now_add=True)
- `updated_at` (DateTimeField, auto_now=True)

**Indexes:**
- title
- genre
- release_date

**Ordering:** -release_date

---

### 2. **Scene Model** (`apps.scene.models.Scene`)
Stores individual scenes from movies with timing and content information.

**Fields:**
- `id` (BigAutoField, Primary Key)
- `movie` (ForeignKey → Movie, CASCADE)
- `title` (CharField, max_length=255)
- `description` (TextField)
- `scene_type` (CharField, choices: action, dialogue, montage, transition, exposition, climax, other)
- `start_time_seconds` (IntegerField, validated: ≥ 0)
- `end_time_seconds` (IntegerField, validated: ≥ 0)
- `duration_seconds` (IntegerField, auto-calculated)
- `location` (CharField, max_length=255, optional)
- `characters` (TextField, optional)
- `transcript` (TextField, optional)
- `scene_number` (IntegerField)
- `emotional_intensity` (IntegerField, 1-10 scale, default=5)
- `key_moments` (BooleanField, default=False)
- `tags` (CharField, max_length=500, optional)
- `thumbnail_url` (URLField, optional)
- `video_url` (URLField, optional)
- `created_at` (DateTimeField, auto_now_add=True)
- `updated_at` (DateTimeField, auto_now=True)

**Unique Constraints:**
- (movie, scene_number)

**Indexes:**
- (movie, scene_number)
- scene_type
- key_moments

**Ordering:** movie, scene_number

---

### 3. **SceneAnalysis Model** (`apps.analysis.models.SceneAnalysis`)
Stores analysis data for individual scenes.

**Fields:**
- `id` (BigAutoField, Primary Key)
- `scene` (ForeignKey → Scene, CASCADE)
- `analysis_type` (CharField, choices: emotional, visual, audio, pacing, narrative, cinematography, other)
- `score` (FloatField, 0-10 scale)
- `confidence` (FloatField, 0-1 scale)
- `summary` (TextField)
- `detailed_findings` (JSONField)
- `analyzed_by` (CharField, max_length=100, optional)
- `methodology` (CharField, max_length=255, optional)
- `data_source` (CharField, max_length=255, optional)
- `created_at` (DateTimeField, auto_now_add=True)
- `updated_at` (DateTimeField, auto_now=True)

**Unique Constraints:**
- (scene, analysis_type)

**Indexes:**
- (scene, analysis_type)
- analysis_type
- score

**Ordering:** -created_at

---

### 4. **MovieAnalysis Model** (`apps.analysis.models.MovieAnalysis`)
Stores high-level analysis for entire movies.

**Fields:**
- `id` (BigAutoField, Primary Key)
- `movie` (ForeignKey → Movie, CASCADE)
- `analysis_type` (CharField, choices: structure, themes, character, production, audience, critical, other)
- `rating` (FloatField, 0-10 scale)
- `title` (CharField, max_length=255)
- `description` (TextField)
- `findings` (JSONField)
- `analyst` (CharField, max_length=100, optional)
- `methodology` (CharField, max_length=255, optional)
- `created_at` (DateTimeField, auto_now_add=True)
- `updated_at` (DateTimeField, auto_now=True)

**Unique Constraints:**
- (movie, analysis_type)

**Indexes:**
- (movie, analysis_type)
- analysis_type
- rating

**Ordering:** -created_at

---

### 5. **AnalysisMetric Model** (`apps.analysis.models.AnalysisMetric`)
Stores detailed metrics for scene analysis.

**Fields:**
- `id` (BigAutoField, Primary Key)
- `scene_analysis` (ForeignKey → SceneAnalysis, CASCADE)
- `metric_name` (CharField, max_length=255)
- `value` (FloatField)
- `unit` (CharField, max_length=50, optional)
- `description` (TextField, optional)
- `threshold_min` (FloatField, optional)
- `threshold_max` (FloatField, optional)
- `created_at` (DateTimeField, auto_now_add=True)

**Indexes:**
- (scene_analysis, metric_name)

**Ordering:** metric_name

---

## Database Relationships

```
Movie (1) ──┬──→ (N) Scene
            │
            └──→ (N) MovieAnalysis
                    
Scene (1) ──→ (N) SceneAnalysis (1) ──→ (N) AnalysisMetric
```

---

## Migration Status

All migrations have been successfully applied:

✅ movies.0001_initial - Create Movie model
✅ scene.0001_initial - Create Scene model
✅ analysis.0001_initial - Create SceneAnalysis, MovieAnalysis, and AnalysisMetric models

---

## Admin Interface Configuration

All models are registered in Django admin with custom admin classes:

- **MovieAdmin**: Display movies with filtering by genre, release date, and country
- **SceneAdmin**: Display scenes with filtering by type, key moments, and movie
- **SceneAnalysisAdmin**: Display scene analyses with inline metric editing
- **MovieAnalysisAdmin**: Display movie analyses
- **AnalysisMetricAdmin**: Display individual metrics

Access the admin interface at: `http://localhost:8000/admin/`

---

## Getting Started

### 1. Create a Superuser
```bash
python manage.py createsuperuser
```

### 2. Run Development Server
```bash
python manage.py runserver
```

### 3. Access Admin Interface
Navigate to: `http://localhost:8000/admin/`

### 4. Add Data
- Create movies via admin
- Create scenes for each movie
- Add analysis data for scenes and movies
- Track metrics for detailed analysis

---

## Database Configuration

Current settings use Django's default SQLite database:
- Database: `db.sqlite3`
- Location: Project root directory

To switch to PostgreSQL, update DATABASES in `scenceIQ/settings.py`

---

## Next Steps

1. Create serializers for API endpoints
2. Create views/viewsets for API endpoints
3. Add search functionality
4. Create API documentation
5. Add authentication and permissions
