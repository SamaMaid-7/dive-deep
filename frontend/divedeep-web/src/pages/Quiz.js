import React, { useContext, useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ThemeContext } from '../App';
import { getActiveSession, saveActiveSession } from '../utils/storage';

const API = 'http://127.0.0.1:5000';

function Quiz() {
  const { sessionId } = useParams();
  const navigate = useNavigate();
  const { darkMode, setDarkMode } = useContext(ThemeContext);

  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});

  useEffect(() => {
    fetch(`${API}/sessions/${sessionId}/quiz`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Unable to load quiz');
        }
        return res.json();
      })
      .then((data) => {
        setQuestions(data);
        const active = getActiveSession();
        if (
          active &&
          Number(active.sessionId) === Number(sessionId) &&
          typeof active.quizIndex === 'number'
        ) {
          setCurrentIndex(active.quizIndex);
          setAnswers(active.quizAnswers || {});
        }
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'Something went wrong.');
        setLoading(false);
      });
  }, [sessionId]);

  const currentQuestion = questions[currentIndex];
  const selected = currentQuestion ? answers[currentQuestion.id] : null;

  const options = useMemo(() => {
    if (!currentQuestion) {
      return [];
    }
    return [
      { key: 'a', label: currentQuestion.option_a },
      { key: 'b', label: currentQuestion.option_b },
      { key: 'c', label: currentQuestion.option_c },
      { key: 'd', label: currentQuestion.option_d }
    ];
  }, [currentQuestion]);

  useEffect(() => {
    if (!questions.length) {
      return;
    }
    const active = getActiveSession();
    saveActiveSession({
      sessionId: Number(sessionId),
      categoryId: active?.categoryId || null,
      categoryName: active?.categoryName || '',
      sessionTitle: active?.sessionTitle || `Session ${sessionId}`,
      route: `/quiz/${sessionId}`,
      progressText: `Quiz Q${currentIndex + 1}`,
      quizIndex: currentIndex,
      quizAnswers: answers
    });
  }, [sessionId, currentIndex, questions.length, answers]);

  const pickAnswer = (optionKey) => {
    if (!currentQuestion) {
      return;
    }
    setAnswers((prev) => ({
      ...prev,
      [currentQuestion.id]: optionKey
    }));
  };

  const goNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  const goBack = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const canSubmit = questions.length > 0 && Object.keys(answers).length === questions.length;

  const submitQuiz = () => {
    if (!canSubmit) {
      return;
    }

    let correct = 0;
    const resultDetails = questions.map((question) => {
      const userAnswer = answers[question.id];
      const isCorrect = userAnswer === question.correct_option;
      if (isCorrect) {
        correct += 1;
      }
      return {
        question_id: question.id,
        question: question.question,
        your_answer: userAnswer,
        correct_answer: question.correct_option,
        is_correct: isCorrect,
        option_a: question.option_a,
        option_b: question.option_b,
        option_c: question.option_c,
        option_d: question.option_d
      };
    });

    const total = questions.length;
    const wrong = total - correct;
    const scorePercentage = total ? Math.round((correct / total) * 100) : 0;

    navigate(`/result/${sessionId}`, {
      state: {
        total,
        correct,
        wrong,
        score_percentage: scorePercentage,
        result_details: resultDetails
      }
    });
  };

  if (loading) {
    return (
      <div className="center-screen">
        <div className="loader"></div>
        <p>Preparing quiz...</p>
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

  if (!questions.length) {
    return (
      <div className="center-screen">
        <p>No quiz questions found for this session.</p>
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

      <div className="top-actions">
        <button className="btn-secondary full-width" onClick={() => navigate('/')}>
          Home
        </button>
      </div>

      <div className="progress-shell">
        <div className="progress-label">
          Question {currentIndex + 1} of {questions.length}
        </div>
        <div className="progress-track">
          <div
            className="progress-fill"
            style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
          ></div>
        </div>
      </div>

      <div className="quiz-card">
        <div className="session-tag">Quiz</div>
        <h2 className="quiz-question">{currentQuestion.question}</h2>

        <div className="quiz-options">
          {options.map((option) => (
            <button
              key={option.key}
              className={`quiz-option ${selected === option.key ? 'selected' : ''}`}
              onClick={() => pickAnswer(option.key)}
            >
              <span className="option-badge">{option.key.toUpperCase()}</span>
              <span>{option.label}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="quiz-actions">
        <button className="btn-secondary" onClick={goBack} disabled={currentIndex === 0}>
          ← Back
        </button>
        {currentIndex < questions.length - 1 ? (
          <button className="btn-primary" onClick={goNext} disabled={!selected}>
            Next →
          </button>
        ) : (
          <button className="btn-primary" onClick={submitQuiz} disabled={!canSubmit}>
            Submit Quiz
          </button>
        )}
      </div>
    </>
  );
}

export default Quiz;
