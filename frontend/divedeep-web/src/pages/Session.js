import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ThemeContext } from '../App';
import { saveActiveSession } from '../utils/storage';

const API = 'http://127.0.0.1:5000';

function Session() {
  const { categoryId } = useParams();
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const { darkMode, setDarkMode } = useContext(ThemeContext);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${API}/sessions?category_id=${categoryId}`)
      .then(res => res.json())
      .then(data => {
        const categorySessions = data.filter(s => s.category_id === parseInt(categoryId));
        if (categorySessions.length > 0) {
          const random = categorySessions[Math.floor(Math.random() * categorySessions.length)];
          setSession(random);
        }
        setLoading(false);
      })
      .catch(err => {
        console.log(err);
        setLoading(false);
      });
  }, [categoryId]);

  if (loading) return (
    <div className="center-screen">
      <div className="loader"></div>
      <p>Finding your session...</p>
    </div>
  );

  if (!session) return (
    <div className="center-screen">
      <p>No sessions found for this category.</p>
      <button className="btn-primary" onClick={() => navigate('/')}>Go Back</button>
    </div>
  );

  return (
    <>
      {/* HEADER */}
      <div className="header">
        <div className="menu-btn" onClick={() => navigate('/')}>←</div>
        <div className="logo">dive<span>deep</span></div>
        <div className="theme-btn" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? '☀️' : '🌙'}
        </div>
      </div>

      <div className="top-actions">
        <button className="btn-secondary full-width" onClick={() => navigate('/')}>
          Home
        </button>
      </div>

      {/* SESSION CARD */}
      <div className="session-hero">
        <div className="session-tag">New Session</div>
        <h1 className="session-hero-title">{session.title}</h1>
        <p className="session-hero-sub">2 lessons · Quick quiz · ~5 mins</p>
      </div>

      {/* SESSION INFO */}
      <div className="info-cards">
        <div className="info-card">
          <div className="info-icon">📖</div>
          <div className="info-label">Lessons</div>
          <div className="info-value">2</div>
        </div>
        <div className="info-card">
          <div className="info-icon">🧩</div>
          <div className="info-label">Quiz</div>
          <div className="info-value">3-5 Q</div>
        </div>
        <div className="info-card">
          <div className="info-icon">⏱️</div>
          <div className="info-label">Time</div>
          <div className="info-value">~5 min</div>
        </div>
      </div>

      {/* START BUTTON */}
      <button
        className="btn-primary full-width"
        onClick={() => {
          saveActiveSession({
            sessionId: session.id,
            categoryId: Number(categoryId),
            sessionTitle: session.title,
            route: `/lesson/${session.id}/1`,
            progressText: 'Lesson 1'
          });
          navigate(`/lesson/${session.id}/1`);
        }}
      >
        Start Session →
      </button>
    </>
  );
}

export default Session;