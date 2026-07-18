/**
 * SceneIQ Frontend API Layer
 *
 * Complete mapping of all Django REST Framework backend endpoints.
 * Vite dev-server proxies `/api` → `http://localhost:8000` (see vite.config.js).
 *
 * Organisation:
 *   1. Shared helpers
 *   2. Movies API        – /api/movies/
 *   3. Scenes API        – /api/scenes/
 *   4. Analysis API      – /api/analysis/
 */

// ---------------------------------------------------------------------------
// 1. Shared helpers
// ---------------------------------------------------------------------------

/**
 * Build a query-string from an object, omitting null / undefined / '' values.
 * @param {Record<string, any>} params
 * @returns {string} e.g. "?genre=action&page=2" or "" if empty
 */
const buildQuery = (params = {}) => {
  const entries = Object.entries(params).filter(
    ([, v]) => v !== null && v !== undefined && v !== '',
  );
  if (entries.length === 0) return '';
  return '?' + new URLSearchParams(entries).toString();
};

/**
 * Central response handler — throws a descriptive error on non-2xx responses.
 * @param {Response} response
 * @returns {Promise<any>} parsed JSON body
 */
const handleResponse = async (response) => {
  if (!response.ok) {
    let detail;
    try {
      const body = await response.json();
      // DRF may return { detail: "..." } or { error: "..." } or field errors
      detail = body.detail || body.error || JSON.stringify(body);
    } catch {
      detail = await response.text().catch(() => response.statusText);
    }
    const err = new Error(detail);
    err.status = response.status;
    throw err;
  }
  return response.json();
};

/** Standard headers for JSON POST / PUT / PATCH requests. */
const JSON_HEADERS = { 'Content-Type': 'application/json' };

/** Base fetch options shared across all calls. */
const BASE_OPTS = { credentials: 'same-origin' };

// ---------------------------------------------------------------------------
// 2. Movies API — /api/movies/
// ---------------------------------------------------------------------------

/**
 * List / search movies.
 *
 * The backend `MovieViewSet.list()` proxies to the OMDb external API and
 * returns: `{ page, total_results, results: [...] }`
 *
 * @param {Object}  [params]
 * @param {string}  [params.q]         - Search query (defaults to "movie" on backend)
 * @param {string}  [params.platform]  - Filter by platform: netflix | prime | hulu
 * @param {number}  [params.year]      - Release year filter
 * @param {number}  [params.page]      - Page number (default 1)
 * @returns {Promise<{ page: number, total_results: number, results: Array }>}
 */
export const getMovies = (params = {}) =>
  fetch(`/api/movies/${buildQuery(params)}`, BASE_OPTS).then(handleResponse);

/**
 * Get full details for a single movie (from local DB).
 *
 * Returns the MovieDetailSerializer shape including streaming_urls.
 *
 * @param {number|string} id - Movie primary key
 * @returns {Promise<Object>}
 */
export const getMovieDetails = (id) =>
  fetch(`/api/movies/${id}/`, BASE_OPTS).then(handleResponse);

/**
 * Get movies filtered by genre (from local DB).
 *
 * @param {string} genre - One of: action, comedy, drama, horror, sci-fi, fantasy,
 *                          thriller, romance, documentary, other
 * @returns {Promise<Array>}
 */
export const getMoviesByGenre = (genre) =>
  fetch(`/api/movies/by_genre/${buildQuery({ genre })}`, BASE_OPTS).then(handleResponse);

/**
 * Get movies available on a specific streaming platform (from local DB).
 *
 * @param {string} platform - One of: netflix, prime, hulu
 * @returns {Promise<Array>}
 */
export const getStreamingAvailable = (platform) =>
  fetch(`/api/movies/streaming_available/${buildQuery({ platform })}`, BASE_OPTS).then(
    handleResponse,
  );

/**
 * Get top-rated movies ordered by IMDb rating (from local DB).
 *
 * @param {number} [limit=10]
 * @returns {Promise<Array>}
 */
export const getTopRatedMovies = (limit = 10) =>
  fetch(`/api/movies/top_rated/${buildQuery({ limit })}`, BASE_OPTS).then(handleResponse);

/**
 * Search for movies on OMDb (external API, no DB write).
 *
 * Returns: `{ page, total_results, results: [{ imdb_id, title, year, poster_url, type }] }`
 *
 * @param {string} query
 * @param {Object} [opts]
 * @param {string} [opts.platform]
 * @param {number} [opts.year]
 * @returns {Promise<Object>}
 */
export const searchMoviesExternal = (query, { platform, year } = {}) =>
  fetch(
    `/api/movies/external_search/${buildQuery({ q: query, platform, year })}`,
    BASE_OPTS,
  ).then(handleResponse);

/**
 * Import a movie from OMDb into the local database.
 *
 * @param {string} imdbId - e.g. "tt1375666"
 * @returns {Promise<Object>} The created MovieDetailSerializer data
 */
export const importMovie = (imdbId) =>
  fetch('/api/movies/import_external/', {
    ...BASE_OPTS,
    method: 'POST',
    headers: JSON_HEADERS,
    body: JSON.stringify({ imdb_id: imdbId }),
  }).then(handleResponse);

/**
 * Get all streaming URLs for a specific movie.
 *
 * @param {number|string} movieId
 * @returns {Promise<{ netflix: string|null, prime_video: string|null, hulu: string|null }>}
 */
export const getStreamingUrls = (movieId) =>
  fetch(`/api/movies/${movieId}/streaming_urls/`, BASE_OPTS).then(handleResponse);

/**
 * Update a movie (full replacement).
 *
 * @param {number|string} id
 * @param {Object} data - MovieCreateUpdateSerializer fields
 * @returns {Promise<Object>}
 */
export const updateMovie = (id, data) =>
  fetch(`/api/movies/${id}/`, {
    ...BASE_OPTS,
    method: 'PUT',
    headers: JSON_HEADERS,
    body: JSON.stringify(data),
  }).then(handleResponse);

/**
 * Partially update a movie.
 *
 * @param {number|string} id
 * @param {Object} data - Subset of MovieCreateUpdateSerializer fields
 * @returns {Promise<Object>}
 */
export const patchMovie = (id, data) =>
  fetch(`/api/movies/${id}/`, {
    ...BASE_OPTS,
    method: 'PATCH',
    headers: JSON_HEADERS,
    body: JSON.stringify(data),
  }).then(handleResponse);

/**
 * Delete a movie.
 *
 * @param {number|string} id
 * @returns {Promise<void>}
 */
export const deleteMovie = (id) =>
  fetch(`/api/movies/${id}/`, { ...BASE_OPTS, method: 'DELETE' }).then((res) => {
    if (!res.ok) throw new Error(`Delete failed: ${res.status}`);
  });

// ---------------------------------------------------------------------------
// 3. Scenes API — /api/scenes/
// ---------------------------------------------------------------------------

/**
 * List scenes with optional DRF filters.
 *
 * Paginated response: `{ count, next, previous, results: [...] }`
 *
 * @param {Object}  [params]
 * @param {number}  [params.movie]        - Filter by movie ID
 * @param {string}  [params.scene_type]   - action | dialogue | montage | transition | exposition | climax | other
 * @param {boolean} [params.key_moments]  - true / false
 * @param {string}  [params.search]       - Full-text search
 * @param {string}  [params.ordering]     - e.g. "-emotional_intensity"
 * @param {number}  [params.page]         - Page number
 * @returns {Promise<Object>}
 */
export const getScenes = (params = {}) =>
  fetch(`/api/scenes/${buildQuery(params)}`, BASE_OPTS).then(handleResponse);

/**
 * Get full details for a single scene.
 *
 * @param {number|string} id
 * @returns {Promise<Object>}
 */
export const getSceneDetails = (id) =>
  fetch(`/api/scenes/${id}/`, BASE_OPTS).then(handleResponse);

/**
 * Get all scenes belonging to a specific movie (custom action).
 *
 * Returns a flat array (no pagination wrapper).
 *
 * @param {number|string} movieId
 * @returns {Promise<Array>}
 */
export const getScenesByMovie = (movieId) =>
  fetch(`/api/scenes/by_movie/${buildQuery({ movie_id: movieId })}`, BASE_OPTS).then(
    handleResponse,
  );

/**
 * Get all key moments (scenes marked as notable) across all movies.
 *
 * @returns {Promise<Array>}
 */
export const getKeyMoments = () =>
  fetch('/api/scenes/key_moments/', BASE_OPTS).then(handleResponse);

/**
 * Get scenes filtered by scene type.
 *
 * @param {string} type - action | dialogue | montage | transition | exposition | climax | other
 * @returns {Promise<Array>}
 */
export const getScenesByType = (type) =>
  fetch(`/api/scenes/by_type/${buildQuery({ type })}`, BASE_OPTS).then(handleResponse);

/**
 * Get scenes filtered by emotional intensity range.
 *
 * @param {number} [min=1]  - Minimum intensity (1-10)
 * @param {number} [max=10] - Maximum intensity (1-10)
 * @returns {Promise<Array>}
 */
export const getScenesByIntensity = (min = 1, max = 10) =>
  fetch(`/api/scenes/emotional_intensity/${buildQuery({ min, max })}`, BASE_OPTS).then(
    handleResponse,
  );

/**
 * Create a new scene.
 *
 * @param {Object} data - SceneCreateUpdateSerializer fields
 * @returns {Promise<Object>}
 */
export const createScene = (data) =>
  fetch('/api/scenes/', {
    ...BASE_OPTS,
    method: 'POST',
    headers: JSON_HEADERS,
    body: JSON.stringify(data),
  }).then(handleResponse);

/**
 * Update a scene (full replacement).
 *
 * @param {number|string} id
 * @param {Object} data
 * @returns {Promise<Object>}
 */
export const updateScene = (id, data) =>
  fetch(`/api/scenes/${id}/`, {
    ...BASE_OPTS,
    method: 'PUT',
    headers: JSON_HEADERS,
    body: JSON.stringify(data),
  }).then(handleResponse);

/**
 * Partially update a scene.
 *
 * @param {number|string} id
 * @param {Object} data
 * @returns {Promise<Object>}
 */
export const patchScene = (id, data) =>
  fetch(`/api/scenes/${id}/`, {
    ...BASE_OPTS,
    method: 'PATCH',
    headers: JSON_HEADERS,
    body: JSON.stringify(data),
  }).then(handleResponse);

/**
 * Delete a scene.
 *
 * @param {number|string} id
 * @returns {Promise<void>}
 */
export const deleteScene = (id) =>
  fetch(`/api/scenes/${id}/`, { ...BASE_OPTS, method: 'DELETE' }).then((res) => {
    if (!res.ok) throw new Error(`Delete failed: ${res.status}`);
  });

// ---------------------------------------------------------------------------
// 4. Analysis API — /api/analysis/
// ---------------------------------------------------------------------------

/**
 * Analyze arbitrary scene text.
 *
 * @param {Object} payload
 * @param {string} payload.text                - Scene text to analyze (required)
 * @param {string} [payload.scene_title]       - Optional title
 * @param {string[]} [payload.analysis_types]  - Subset of:
 *   "emotional", "visual", "audio", "pacing", "narrative", "cinematography"
 *   Defaults to ["emotional", "visual", "audio"] on backend.
 * @returns {Promise<Object>} Analysis response with analyses, metrics, processing_time_seconds
 */
export const analyzeScene = (payload) =>
  fetch('/api/analysis/analyze/', {
    ...BASE_OPTS,
    method: 'POST',
    headers: JSON_HEADERS,
    body: JSON.stringify(payload),
  }).then(handleResponse);

/**
 * Generate scenes for a movie and optionally analyze them immediately.
 *
 * @param {Object} payload
 * @param {number} payload.movie_id            - Movie PK (required)
 * @param {number} [payload.num_scenes=3]      - Number of scenes to generate
 * @param {boolean} [payload.analyze_scenes]   - Run analysis on generated scenes (default false)
 * @returns {Promise<Object>} { movie_id, movie_title, scenes_created, scenes, analyses? }
 */
export const generateScenes = (payload) =>
  fetch('/api/analysis/generate-scenes/', {
    ...BASE_OPTS,
    method: 'POST',
    headers: JSON_HEADERS,
    body: JSON.stringify(payload),
  }).then(handleResponse);

/**
 * Analyze all existing scenes for a movie.
 *
 * @param {Object} payload
 * @param {number} payload.movie_id            - Movie PK (required)
 * @param {string[]} [payload.analysis_types]  - Analysis types to run
 * @returns {Promise<Object>} { movie_id, movie_title, scenes_analyzed, total_scenes, analyses }
 */
export const analyzeMovieScenes = (payload) =>
  fetch('/api/analysis/analyze-movie-scenes/', {
    ...BASE_OPTS,
    method: 'POST',
    headers: JSON_HEADERS,
    body: JSON.stringify(payload),
  }).then(handleResponse);
