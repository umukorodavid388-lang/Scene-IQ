# SceneIQ Frontend Documentation

This document provides a comprehensive guide to the SceneIQ frontend architecture, API integration, and development workflow. It serves as the primary reference for frontend developers working on this project.

## 1. Project Overview & Tech Stack

The SceneIQ frontend is a React application built with Vite. It serves as the user interface for the Django REST Framework (DRF) backend, allowing users to browse movies, generate scenes, and run comprehensive textual and cinematic analysis.

**Core Technologies:**
- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** Vanilla CSS (`styles.css`), designed for a dark-mode, modern aesthetic.
- **API Communication:** Native `fetch` API via a centralized `api.js` service.
- **Backend Proxy:** Vite proxy to avoid CORS issues during development.

## 2. Folder Structure

```
frontend/
├── index.html            # Main HTML entry point
├── package.json          # Dependencies and scripts
├── vite.config.js        # Vite configuration (includes API proxy)
└── src/
    ├── api.js            # Centralized API service layer
    ├── App.jsx           # Root application component
    ├── main.jsx          # React DOM mounting
    └── styles.css        # Global styles and design system
```

## 3. Development Workflow

### Starting the Dev Server
The frontend is designed to run concurrently with the Django backend.

1. Ensure the Django backend is running:
   ```bash
   cd scenceIQ
   python manage.py runserver
   ```
   (Backend runs on `http://localhost:8000`)

2. Start the Vite frontend server:
   ```bash
   cd frontend
   npm run dev
   ```
   (Frontend runs on `http://localhost:5173`)

### Vite Proxy Configuration
To simplify development and avoid Cross-Origin Resource Sharing (CORS) setup on the backend, `vite.config.js` is configured to proxy all `/api` requests to the Django server:

```javascript
// vite.config.js
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
```
*Note: In a production environment, you will either need to serve the frontend from Django or configure CORS correctly on the Django backend.*

## 4. API Layer (`src/api.js`)

The `api.js` file contains wrapper functions for **every** endpoint exposed by the Django backend. All functions use native `fetch`, handle errors consistently, and format query strings correctly.

### 4.1. Core Concepts
- **Credentials:** All requests include `credentials: 'same-origin'` to ensure cookies (like CSRF tokens or session IDs) are sent if authentication is implemented later.
- **Error Handling:** Non-2xx responses throw an Error containing the message provided by the DRF backend.
- **Query Building:** A utility `buildQuery()` drops empty/null parameters to ensure clean URLs.

### 4.2. Movies API Mapping (`/api/movies/`)

| Frontend Function | Backend Endpoint | Method | Purpose |
|-------------------|------------------|--------|---------|
| `getMovies({ q, platform, year, page })` | `/api/movies/` | GET | List/search movies (proxies to OMDb via backend) |
| `getMovieDetails(id)` | `/api/movies/{id}/` | GET | Get full movie details from DB |
| `getMoviesByGenre(genre)` | `/api/movies/by_genre/?genre=...` | GET | Filter DB movies by genre |
| `getStreamingAvailable(platform)` | `/api/movies/streaming_available/?platform=...` | GET | Filter DB movies by platform |
| `getTopRatedMovies(limit)` | `/api/movies/top_rated/?limit=...` | GET | Get highest rated movies |
| `searchMoviesExternal(query, { platform, year })` | `/api/movies/external_search/?q=...` | GET | Direct search to OMDb |
| `importMovie(imdbId)` | `/api/movies/import_external/` | POST | Import an OMDb movie into the DB |
| `getStreamingUrls(id)` | `/api/movies/{id}/streaming_urls/` | GET | Get just the streaming links |
| `updateMovie(id, data)` | `/api/movies/{id}/` | PUT | Full update |
| `patchMovie(id, data)` | `/api/movies/{id}/` | PATCH | Partial update |
| `deleteMovie(id)` | `/api/movies/{id}/` | DELETE | Delete a movie |

### 4.3. Scenes API Mapping (`/api/scenes/`)

| Frontend Function | Backend Endpoint | Method | Purpose |
|-------------------|------------------|--------|---------|
| `getScenes(params)` | `/api/scenes/` | GET | List/filter scenes (paginated) |
| `getSceneDetails(id)` | `/api/scenes/{id}/` | GET | Get single scene details |
| `getScenesByMovie(movieId)` | `/api/scenes/by_movie/?movie_id=...` | GET | Get all scenes for a movie |
| `getKeyMoments()` | `/api/scenes/key_moments/` | GET | Get all notable scenes |
| `getScenesByType(type)` | `/api/scenes/by_type/?type=...` | GET | Filter scenes by type |
| `getScenesByIntensity(min, max)` | `/api/scenes/emotional_intensity/?min=...` | GET | Filter by intensity range |
| `createScene(data)` | `/api/scenes/` | POST | Create a new scene manually |
| `updateScene(id, data)` | `/api/scenes/{id}/` | PUT | Full update |
| `patchScene(id, data)` | `/api/scenes/{id}/` | PATCH | Partial update |
| `deleteScene(id)` | `/api/scenes/{id}/` | DELETE | Delete a scene |

### 4.4. Analysis API Mapping (`/api/analysis/`)

| Frontend Function | Backend Endpoint | Method | Purpose |
|-------------------|------------------|--------|---------|
| `analyzeScene({ text, scene_title, analysis_types })` | `/api/analysis/analyze/` | POST | Analyze raw text |
| `generateScenes({ movie_id, num_scenes, analyze_scenes })` | `/api/analysis/generate-scenes/` | POST | Generate scenes for a movie |
| `analyzeMovieScenes({ movie_id, analysis_types })` | `/api/analysis/analyze-movie-scenes/` | POST | Analyze all existing scenes for a movie |

## 5. Data Structures & Response Shapes

### Pagination Handling
Standard DRF list endpoints return:
```json
{
  "count": 150,
  "next": "http://...",
  "previous": null,
  "results": [{...}]
}
```

However, the main `getMovies()` endpoint proxies to OMDb and returns:
```json
{
  "page": 1,
  "total_results": 100,
  "results": [{...}]
}
```

**Implementation Note:** When rendering lists, always access the `results` array safely. See `App.jsx` for an example of handling multiple response shapes robustly.

### Models

**Movie Detail Shape:**
```javascript
{
  id: 123,
  title: "Inception",
  description: "...",
  genre: "action",
  release_date: "2010-07-16",
  imdb_rating: 8.8,
  poster_url: "https://...",
  streaming_urls: {
    netflix: null,
    prime_video: "https://...",
    hulu: null
  }
}
```

**Scene Detail Shape:**
```javascript
{
  id: 1,
  movie: 123,
  movie_title: "Inception",
  title: "Opening Sequence",
  scene_type: "action",
  start_time_seconds: 0,
  duration_seconds: 180,
  emotional_intensity: 8,
  key_moments: true
}
```

**Analysis Response Shape:**
```javascript
{
  scene_title: "Confrontation",
  text_length: 245,
  analyses: [
    {
      analysis_type: "emotional",
      score: 8.5,
      confidence: 0.85,
      summary: "...",
      detailed_findings: { ... }
    }
  ],
  processing_time_seconds: 0.045
}
```

## 6. Coding Conventions

1. **State Management:** Use standard React hooks (`useState`, `useEffect`). For complex state, consider React Query (if added later) to manage caching and loading states for API calls.
2. **Styling:** CSS uses a global `styles.css` tailored for a premium dark mode. Stick to the defined color palette (`#0f172a`, `#e2e8f0`, etc.).
3. **Component Structure:** If expanding the app, create a `components/` folder for reusable UI pieces (e.g., `MovieCard.jsx`, `SceneList.jsx`) and a `pages/` folder for view-level components.
4. **API Calls:** Never use `fetch` directly in components. Always import the relevant function from `api.js`.

---
*End of Documentation*
