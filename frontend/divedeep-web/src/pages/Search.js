import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getLessonHistory } from '../utils/storage';

const API = 'http://127.0.0.1:5000';

function Search() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [sessions, setSessions] = useState([]);
  const [categoriesMap, setCategoriesMap] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([
      fetch(`${API}/categories`).then((res) => res.json()),
      fetch(`${API}/sessions`).then((res) => res.json())
    ])
      .then(([categories, sessionsData]) => {
        const map = categories.reduce((acc, item) => {
          acc[item.id] = item.name;
          return acc;
        }, {});
        setCategoriesMap(map);
        setSessions(sessionsData);
        setLoading(false);
      })
      .catch(() => {
        setError('Unable to load search data.');
        setLoading(false);
      });
  }, []);

  const completedSessionIds = useMemo(() => {
    const history = getLessonHistory();
    return new Set(history.map((item) => Number(item.sessionId)));
  }, []);

  const filtered = useMemo(() => {
    const value = query.trim().toLowerCase();
    const enriched = sessions.map((session) => ({
      ...session,
      categoryName: categoriesMap[session.category_id] || 'General'
    }));

    const searched = !value
      ? enriched
      : enriched.filter((item) =>
          `${item.categoryName} ${item.title}`.toLowerCase().includes(value)
        );

    return searched.sort((a, b) => a.title.localeCompare(b.title));
  }, [query, sessions, categoriesMap]);

  return (
    <>
      <div className="header">
        <div className="menu-btn" onClick={() => navigate('/')}>
          ←
        </div>
        <div className="logo">
          Search<span>Sessions</span>
        </div>
        <div className="theme-btn" onClick={() => navigate('/')}>
          ⌂
        </div>
      </div>

      <div className="search-shell">
        <input
          className="search-input"
          placeholder="Search by category or session..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {loading && (
        <div className="center-screen">
          <div className="loader"></div>
          <p>Loading sessions...</p>
        </div>
      )}

      {error && (
        <div className="center-screen">
          <p>{error}</p>
          <button className="btn-primary" onClick={() => navigate('/')}>
            Go Home
          </button>
        </div>
      )}

      {!loading && !error && (
        <div className="search-results">
          {!filtered.length && <p className="small-note">No matching sessions found.</p>}
          {filtered.map((item) => {
            const completed = completedSessionIds.has(Number(item.id));
            return (
              <div
                key={item.id}
                className={`search-card ${completed ? 'completed' : 'incomplete'}`}
                onClick={() => navigate(`/session/${item.category_id}`)}
              >
                <div className="search-row">
                  <p className="search-category">{item.categoryName}</p>
                  <span className={`status-badge ${completed ? 'done' : 'todo'}`}>
                    {completed ? 'Completed' : 'New'}
                  </span>
                </div>
                <p className="search-title">{item.title}</p>
              </div>
            );
          })}
        </div>
      )}
    </>
  );
}

export default Search;
