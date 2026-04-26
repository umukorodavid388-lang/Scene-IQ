const handleResponse = async (response) => {
  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error ${response.status}: ${text}`);
  }
  return response.json();
};

export const getMovies = () => fetch('/api/movies/').then(handleResponse);
export const getScenesByMovie = (movieId) =>
  fetch(`/api/scenes/by_movie/?movie_id=${movieId}`).then(handleResponse);
export const analyzeMovie = (payload) =>
  fetch('/api/analysis/analyze/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  }).then(handleResponse);
export const generateScenes = (payload) =>
  fetch('/api/analysis/generate-scenes/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  }).then(handleResponse);
