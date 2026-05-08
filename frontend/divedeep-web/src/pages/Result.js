import React, { useContext } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { ThemeContext } from '../App';

function Result() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { darkMode, setDarkMode } = useContext(ThemeContext);

  const result = location.state;

  if (!result) {
    return (
      <div className="center-screen">
        <p>No result data found. Please complete the quiz first.</p>
        <button className="btn-primary" onClick={() => navigate(`/quiz/${sessionId}`)}>
          Take Quiz
        </button>
      </div>
    );
  }

  const {
    total,
    correct,
    wrong,
    score_percentage: scorePercentage,
    result_details: resultDetails
  } = result;

  const pieStyle = {
    background: `conic-gradient(var(--accent) 0deg ${scorePercentage * 3.6}deg, var(--surface2) ${scorePercentage * 3.6}deg 360deg)`
  };

  const resolveOptionText = (detail, optionKey) => {
    if (!optionKey) {
      return 'Not answered';
    }
    return detail[`option_${optionKey}`] || 'Unknown option';
  };

  return (
    <>
      <div className="header">
        <div className="menu-btn" onClick={() => navigate('/')}>
          ←
        </div>
        <div className="logo">
          dive<span>deep</span>
        </div>
        <div className="theme-btn" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? '☀️' : '🌙'}
        </div>
      </div>

      <div className="result-card">
        <div className="session-tag">Result</div>
        <h1 className="session-hero-title">Great effort!</h1>

        <div className="result-pie-wrap">
          <div className="result-pie" style={pieStyle}>
            <div className="result-pie-center">
              <span>{scorePercentage}%</span>
            </div>
          </div>
        </div>

        <div className="result-stats">
          <div className="result-stat">
            <p className="result-stat-label">Correct</p>
            <p className="result-stat-value">{correct}</p>
          </div>
          <div className="result-stat">
            <p className="result-stat-label">Wrong</p>
            <p className="result-stat-value">{wrong}</p>
          </div>
          <div className="result-stat">
            <p className="result-stat-label">Total</p>
            <p className="result-stat-value">{total}</p>
          </div>
        </div>
      </div>

      <div className="review-section">
        <div className="section-header">
          <span className="section-title">Full Review</span>
          <span className="section-sub">Question by question</span>
        </div>

        <div className="review-list">
          {resultDetails.map((detail, index) => (
            <div key={detail.question_id} className="review-card">
              <p className="review-question">
                Q{index + 1}. {detail.question}
              </p>
              <p className={`review-answer ${detail.is_correct ? 'correct' : 'wrong'}`}>
                Your answer: {resolveOptionText(detail, detail.your_answer)}
              </p>
              <p className="review-correct">
                Correct answer: {resolveOptionText(detail, detail.correct_answer)}
              </p>
            </div>
          ))}
        </div>
      </div>

      <div className="quiz-actions">
        <button className="btn-secondary" onClick={() => navigate(`/quiz/${sessionId}`)}>
          Retry Quiz
        </button>
        <button className="btn-primary" onClick={() => navigate('/')}>
          Go Home
        </button>
      </div>
    </>
  );
}

export default Result;
