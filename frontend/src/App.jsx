import { useEffect, useState } from 'react';
import { getMovies } from './api.js';

export default function App() {
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMovies()
      .then((data) => {
        // The backend MovieViewSet.list() proxies to the OMDb external API
        // and returns: { page, total_results, results: [...] }
        //
        // Standard DRF pagination (for local DB queries) returns:
        // { count, next, previous, results: [...] }
        //
        // Handle both shapes — plus a raw array fallback.
        if (Array.isArray(data)) {
          setMovies(data);
        } else if (data.results) {
          setMovies(data.results);
        } else {
          setMovies([]);
        }
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <div className="app-shell">
      <header>
        <h1>Scene-IQ React Frontend</h1>
        <p>Fetches movie data from the Django API at <code>/api</code>.</p>
      </header>

      <main>
        {loading && <p>Loading movies...</p>}
        {error && <p className="error">{error}</p>}

        {!loading && !error && (
          <section>
            <h2>Movies</h2>
            {movies.length === 0 ? (
              <p>No movies found.</p>
            ) : (
              <ul>
                {movies.map((movie) => (
                  <li key={movie.id || movie.imdb_id}>
                    {movie.title || movie.name}
                  </li>
                ))}
              </ul>
            )}
          </section>
        )}
      </main>
    </div>
  );
}
