const KEYS = {
  profile: 'dd_profile',
  activeSession: 'dd_active_session',
  lessonHistory: 'dd_lesson_history',
  savedLessons: 'dd_saved_lessons'
};

const defaultProfile = {
  fullName: 'DiveDeep Learner',
  username: 'learner01',
  email: 'learner@example.com',
  phone: '+91 90000 00000',
  profilePicture: 'https://i.pravatar.cc/160?img=13',
  bio: 'Learning one short session every day.'
};

function readJson(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    if (!raw) {
      return fallback;
    }
    return JSON.parse(raw);
  } catch (error) {
    return fallback;
  }
}

function writeJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

export function getProfile() {
  return readJson(KEYS.profile, defaultProfile);
}

export function saveProfile(profile) {
  writeJson(KEYS.profile, profile);
}

export function getActiveSession() {
  return readJson(KEYS.activeSession, null);
}

export function saveActiveSession(payload) {
  writeJson(KEYS.activeSession, {
    ...payload,
    updatedAt: new Date().toISOString()
  });
}

export function clearActiveSession() {
  localStorage.removeItem(KEYS.activeSession);
}

export function getLessonHistory() {
  return readJson(KEYS.lessonHistory, []);
}

export function addLessonHistoryItem(item) {
  const current = getLessonHistory();
  const next = [{ ...item, id: crypto.randomUUID() }, ...current];
  writeJson(KEYS.lessonHistory, next.slice(0, 150));
}

export function getSavedLessons() {
  return readJson(KEYS.savedLessons, []);
}

export function isLessonSaved(lessonId) {
  const saved = getSavedLessons();
  return saved.some((item) => item.lessonId === lessonId);
}

export function toggleSavedLesson(lesson) {
  const saved = getSavedLessons();
  const exists = saved.some((item) => item.lessonId === lesson.lessonId);
  let next;

  if (exists) {
    next = saved.filter((item) => item.lessonId !== lesson.lessonId);
  } else {
    next = [{ ...lesson, savedAt: new Date().toISOString() }, ...saved];
  }

  writeJson(KEYS.savedLessons, next);
  return !exists;
}
