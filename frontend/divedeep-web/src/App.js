import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import Session from './pages/Session';
import Lesson from './pages/Lesson';
import Quiz from './pages/Quiz';
import Result from './pages/Result';

export const ThemeContext = React.createContext();

function App() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <ThemeContext.Provider value={{ darkMode, setDarkMode }}>
      <Router>
        <div className={`app ${darkMode ? 'dark' : 'light'}`}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/session/:categoryId" element={<Session />} />
            <Route path="/lesson/:sessionId/:lessonOrder" element={<Lesson />} />
            <Route path="/quiz/:sessionId" element={<Quiz />} />
            <Route path="/result/:sessionId" element={<Result />} />
          </Routes>
        </div>
      </Router>
    </ThemeContext.Provider>
  );
}

export default App;