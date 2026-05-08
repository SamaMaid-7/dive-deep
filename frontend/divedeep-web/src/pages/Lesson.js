import React, { useContext, useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ThemeContext } from '../App';

const API = 'http://127.0.0.1:5000';

function Lesson() {
  const { sessionId, lessonOrder } = useParams();
  const navigate = useNavigate();
  const { darkMode, setDarkMode } = useContext(ThemeContext);

  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch(`${API}/sessions/${sessionId}/lessons`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Unable to load lessons');
        }
        return res.json();
      })
      .then((data) => {
        const sorted = [...data].sort((a, b) => a.order - b.order);
        setLessons(sorted);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'Something went wrong.');
        setLoading(false);
      });
  }, [sessionId]);

  const currentLesson = useMemo(() => {
    const orderNumber = Number(lessonOrder);
    return lessons.find((lesson) => lesson.order === orderNumber);
  }, [lessons, lessonOrder]);

  const currentIndex = currentLesson
    ? lessons.findIndex((lesson) => lesson.id === currentLesson.id)
    : -1;

  const hasNext = currentIndex > -1 && currentIndex < lessons.length - 1;

  const handleNext = () => {
    if (hasNext) {
      const nextLesson = lessons[currentIndex + 1];
      navigate(`/lesson/${sessionId}/${nextLesson.order}`);
      return;
    }
    navigate(`/quiz/${sessionId}`);
  };

  if (loading) {
    return (
      <div className="center-screen">
        <div className="loader"></div>
        <p>Loading lesson...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="center-screen">
        <p>{error}</p>
        <button className="btn-primary" onClick={() => navigate(-1)}>
          Go Back
        </button>
      </div>
    );
  }

  if (!lessons.length || !currentLesson) {
    return (
      <div className="center-screen">
        <p>Lesson not found for this session.</p>
        <button className="btn-primary" onClick={() => navigate('/')}>
          Go Home
        </button>
      </div>
    );
  }

  return (
    <>
      <div className="header">
        <div className="menu-btn" onClick={() => navigate(-1)}>
          ←
        </div>
        <div className="logo">
          dive<span>deep</span>
        </div>
        <div className="theme-btn" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? '☀️' : '🌙'}
        </div>
      </div>

      <div className="progress-shell">
        <div className="progress-label">
          Lesson {currentIndex + 1} of {lessons.length}
        </div>
        <div className="progress-track">
          <div
            className="progress-fill"
            style={{ width: `${((currentIndex + 1) / lessons.length) * 100}%` }}
          ></div>
        </div>
      </div>

      <div className="lesson-card">
        <div className="session-tag">Lesson</div>
        <h1 className="session-hero-title">Key Concept #{currentLesson.order}</h1>
        <p className="lesson-content">{currentLesson.content}</p>
      </div>

      <button className="btn-primary full-width" onClick={handleNext}>
        {hasNext ? 'Next Lesson →' : 'Take Quiz →'}
      </button>
    </>
  );
}

export default Lesson;
