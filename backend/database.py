from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

# USERS TABLE
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    profile_pic = Column(String, nullable=True)
    theme = Column(String, default='light')
    created_at = Column(DateTime, default=datetime.utcnow)

# CATEGORIES TABLE
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

# SESSIONS TABLE
class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

# LESSONS TABLE
class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    order = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)

# QUIZZES TABLE
class Quiz(Base):
    __tablename__ = 'quizzes'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    question = Column(Text, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    option_d = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)

# USER SESSION HISTORY TABLE
class UserSessionHistory(Base):
    __tablename__ = 'user_session_history'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    session_id = Column(Integer, ForeignKey('sessions.id'))
    completed = Column(Boolean, default=False)
    attended_at = Column(DateTime, default=datetime.utcnow)

# SAVED LESSONS TABLE
class SavedLesson(Base):
    __tablename__ = 'saved_lessons'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    lesson_id = Column(Integer, ForeignKey('lessons.id'))
    saved_at = Column(DateTime, default=datetime.utcnow)

# DAILY REMINDER TABLE
class DailyReminder(Base):
    __tablename__ = 'daily_reminders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    reminder_time = Column(String, nullable=False)
    is_auto = Column(Boolean, default=False)

# CREATE ALL TABLES
engine = create_engine('sqlite:///divedeep.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

print("Database created successfully!")