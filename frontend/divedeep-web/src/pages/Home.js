import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { ThemeContext } from '../App';

const API = 'http://127.0.0.1:5000';

const categoryEmojis = {
  Finance: '💰', Beauty: '✨', Politics: '🏛️',
  Science: '🔬', Technology: '⚡', History: '📜',
  Psychology: '🧠', Health: '💚', Philosophy: '🌀', Art: '🎨'
};

function Home() {
  const [categories, setCategories] = useState([]);
  const { darkMode, setDarkMode } = useContext(ThemeContext);
  const navigate = useNavigate();

  useEffect(() => {
    fetch(`${API}/categories`)
      .then(res => res.json())
      .then(data => setCategories(data))
      .catch(err => console.log(err));
  }, []);

  return (
    <>
      {/* HEADER */}
      <div className="header">
        <div className="menu-btn">☰</div>
        <div className="logo">dive<span>deep</span></div>
        <div className="theme-btn" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? '☀️' : '🌙'}
        </div>
      </div>

      {/* ACTIVE SESSION */}
      <div className="active-session inactive">
        <div className="session-indicator"></div>
        <div className="session-text">
          <p className="session-title">No Active Session</p>
          <p className="session-sub">Pick a category below to start learning</p>
        </div>
        <div className="session-arrow">→</div>
      </div>

      {/* CATEGORIES */}
      <div className="section-header">
        <span className="section-title">Explore</span>
        <span className="section-sub">Choose your topic</span>
      </div>

      <div className="categories">
        {categories.map((cat, index) => (
          <div
            key={cat.id}
            className="category-card"
            style={{ animationDelay: `${index * 0.08}s` }}
            onClick={() => navigate(`/session/${cat.id}`)}
          >
            <div className="cat-emoji">
              {categoryEmojis[cat.name] || '📚'}
            </div>
            <div className="cat-name">{cat.name}</div>
            <div className="cat-arrow">→</div>
          </div>
        ))}
      </div>
    </>
  );
}

export default Home;