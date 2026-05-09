import React, { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  getLessonHistory,
  getProfile,
  getSavedLessons,
  saveProfile,
  toggleSavedLesson
} from '../utils/storage';

const tabs = ['account', 'history', 'saved'];

function Profile() {
  const navigate = useNavigate();
  const [tab, setTab] = useState('account');
  const [profile, setProfile] = useState(getProfile());
  const [history, setHistory] = useState(getLessonHistory());
  const [savedLessons, setSavedLessons] = useState(getSavedLessons());
  const [saveMsg, setSaveMsg] = useState('');

  const activeDays = useMemo(() => {
    const days = new Set();
    history.forEach((item) => {
      const day = new Date(item.attendedAt).toISOString().split('T')[0];
      days.add(day);
    });
    return days;
  }, [history]);

  const calendarCells = useMemo(() => {
    const today = new Date();
    const cells = [];
    for (let i = 83; i >= 0; i -= 1) {
      const date = new Date(today);
      date.setDate(today.getDate() - i);
      const key = date.toISOString().split('T')[0];
      cells.push({
        key,
        active: activeDays.has(key)
      });
    }
    return cells;
  }, [activeDays]);

  const updateField = (field, value) => {
    setProfile((prev) => ({ ...prev, [field]: value }));
  };

  const submitProfile = (event) => {
    event.preventDefault();
    saveProfile(profile);
    setSaveMsg('Profile saved locally.');
    setTimeout(() => setSaveMsg(''), 1800);
  };

  const removeSaved = (lesson) => {
    toggleSavedLesson(lesson);
    setSavedLessons(getSavedLessons());
  };

  return (
    <>
      <div className="header">
        <div className="menu-btn" onClick={() => navigate('/')}>
          ←
        </div>
        <div className="logo">
          My<span>Profile</span>
        </div>
        <div className="theme-btn" onClick={() => navigate('/')}>
          ⌂
        </div>
      </div>

      <div className="profile-tabs">
        {tabs.map((item) => (
          <button
            key={item}
            className={`profile-tab ${tab === item ? 'active' : ''}`}
            onClick={() => setTab(item)}
          >
            {item === 'account' && 'My Account'}
            {item === 'history' && 'Lesson History'}
            {item === 'saved' && 'Saved Lessons'}
          </button>
        ))}
      </div>

      {tab === 'account' && (
        <form className="profile-card" onSubmit={submitProfile}>
          <div className="profile-picture-wrap">
            <img src={profile.profilePicture} alt="profile" className="profile-picture" />
          </div>

          <label className="profile-label">Profile Picture URL</label>
          <input
            className="profile-input"
            value={profile.profilePicture}
            onChange={(e) => updateField('profilePicture', e.target.value)}
          />

          <label className="profile-label">Full Name</label>
          <input
            className="profile-input"
            value={profile.fullName}
            onChange={(e) => updateField('fullName', e.target.value)}
          />

          <label className="profile-label">Username</label>
          <input
            className="profile-input"
            value={profile.username}
            onChange={(e) => updateField('username', e.target.value)}
          />

          <label className="profile-label">Email</label>
          <input
            className="profile-input"
            value={profile.email}
            onChange={(e) => updateField('email', e.target.value)}
          />

          <label className="profile-label">Phone Number</label>
          <input
            className="profile-input"
            value={profile.phone}
            onChange={(e) => updateField('phone', e.target.value)}
          />

          <label className="profile-label">Bio</label>
          <textarea
            className="profile-input profile-textarea"
            value={profile.bio}
            onChange={(e) => updateField('bio', e.target.value)}
          />

          <button className="btn-primary full-width" type="submit">
            Save Account
          </button>
          {saveMsg && <p className="small-note">{saveMsg}</p>}
        </form>
      )}

      {tab === 'history' && (
        <div className="profile-card">
          <h3 className="mini-title">Consistency Calendar</h3>
          <p className="small-note">Days with at least one completed session are highlighted.</p>
          <div className="consistency-grid">
            {calendarCells.map((cell) => (
              <div
                key={cell.key}
                className={`consistency-cell ${cell.active ? 'active' : ''}`}
                title={cell.key}
              ></div>
            ))}
          </div>

          <h3 className="mini-title mt-24">Session History</h3>
          {!history.length && <p className="small-note">No completed sessions yet.</p>}
          <div className="history-list">
            {history.map((item) => {
              const date = new Date(item.attendedAt);
              return (
                <div className="history-item" key={item.id}>
                  <p className="history-cat">{item.categoryName || 'General'}</p>
                  <p className="history-snippet">{item.snippet || item.sessionTitle}</p>
                  <p className="history-time">
                    {date.toLocaleDateString()} at {date.toLocaleTimeString()}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {tab === 'saved' && (
        <div className="profile-card">
          <h3 className="mini-title">Saved Lessons</h3>
          {!savedLessons.length && <p className="small-note">No saved lessons yet.</p>}
          <div className="history-list">
            {savedLessons.map((item) => (
              <div className="history-item" key={item.lessonId}>
                <p className="history-cat">{item.categoryName || 'General'}</p>
                <p className="history-snippet">Lesson {item.lessonOrder}: {item.lessonSnippet}</p>
                <div className="saved-actions">
                  <button
                    className="btn-secondary"
                    onClick={() => navigate(`/lesson/${item.sessionId}/${item.lessonOrder}`)}
                  >
                    Open
                  </button>
                  <button className="btn-secondary" onClick={() => removeSaved(item)}>
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}

export default Profile;
