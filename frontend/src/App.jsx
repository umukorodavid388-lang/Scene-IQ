import { useEffect, useState } from 'react';
import { getMovies } from './api.js';

export default function App() {
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMovies()
      .then((data) => {
        setMovies(data.results || data);
      })
      .catch((error) => {
        setError(error.message);
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
                  <li key={movie.id || movie.pk}>{movie.title || movie.name}</li>
                ))}
              </ul>
            )}
          </section>
        )}
      </main>
    </div>
  );
}
